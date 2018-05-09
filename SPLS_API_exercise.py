from flask import request
from flask import jsonify, make_response
from flask import Flask
import datetime

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import csv

# =====================================================


def estimate_price(house_feat):
    price = 0.0
    price += 75.0*house_feat['GrLivArea']
    price += 54.0*house_feat['TotalBsmtSF']
    price += 51.0*house_feat['GarageArea']
    price += 671.0*(house_feat['YearBuilt'] - 1990)

    return price
# =====================================================

# =====================================================


def checkFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
# =====================================================


app = Flask(__name__)


@app.route('/houseprice', methods=["GET"])
def houseprice():
    # Getting paramaters from the request
    GrLivArea = request.args.get('GrLivArea')
    TotalBsmtSF = request.args.get('TotalBsmtSF')
    GarageArea = request.args.get('GarageArea')
    YearBuilt = request.args.get('YearBuilt')

    # Check if all the parameters are provided
    if (GrLivArea is None) or (TotalBsmtSF is None) or (GarageArea is None) or (YearBuilt is None):
        http_response = make_response(jsonify(
            {'Error': 'Please provide all 4 parameters'}
        ))
        return http_response

    # Check if the parameters provided are numeric values or not
    if not (checkFloat(GrLivArea) and checkFloat(TotalBsmtSF) and checkFloat(GarageArea) and checkFloat(YearBuilt)):
        http_response = make_response(jsonify(
            {'Error': 'Please provide numerical parameterss'}
        ))
        return http_response

    # Storing all the values in the List and converting them to int
    house_data = {}
    house_data['GrLivArea'] = int(GrLivArea)
    house_data['TotalBsmtSF'] = int(TotalBsmtSF)
    house_data['GarageArea'] = int(GarageArea)
    house_data['YearBuilt'] = int(YearBuilt)

    thisTime = (datetime.datetime.now())
    thisYear = thisTime.year

    if house_data['YearBuilt'] > thisYear:
        http_response = make_response(jsonify(
            {'Error': 'The year built can''t be greater than current year'}
        ))
        return http_response

    # Check if the parameters provided are positive or not
    for param in house_data.values():
        if param < 0:
            http_response = make_response(jsonify(
                {'Error': 'Please provide positive values of the arguments'}
            ))
            return http_response

    http_response = make_response(jsonify(
        {'HouseFeatures': house_data,
            'PriceEstimate': estimate_price(house_data)}
    ))
    return http_response

# =====================================================


@app.route('/houselookup', methods=["GET"])
def houselookup():
    parameters = request.args

    paramLength = len(parameters)
    # Checking if parameters are odd or even and have at least 3 coordinate values
    if paramLength >= 6 and paramLength % 2 != 0:
        http_response = make_response(jsonify(
            {'Error': 'To make a bounding box, coordinate values should be even in number and >= 6'}
        ))
        return http_response

    boundingBox = []

    for i in range(0, paramLength//2):
        # Checking the paramaters in the format of (x1,y1), (x2,y2) ....
        dictKeyX = 'x' + str(i + 1)
        dictKeyY = 'y' + str(i + 1)

        if dictKeyX in parameters and dictKeyY in parameters:
            if checkFloat(parameters[dictKeyX]) and checkFloat(parameters[dictKeyY]):
                boundingBox.append(
                    (float(parameters[dictKeyX]), float(parameters[dictKeyY])))
                continue

        http_response = make_response(jsonify(
            {'Error': 'Please enter the paramaters in format x1, y1, x2, y2, x3, y3 .... and should be float values'}
        ))
        return http_response

    # Create a polygon
    polygon = Polygon(boundingBox)

    # Now read CSV and check all the points exist or not in the polygon formed above
    with open('house_coordinates.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Skip the header!
        next(readCSV)

        finalHouseIDs = []
        for row in readCSV:
            try:
                # Get all the values from the CSV
                houseId = row[0]
                x1 = float(row[1])
                y1 = float(row[2])
                x2 = float(row[3])
                y2 = float(row[4])
                x3 = float(row[5])
                y3 = float(row[6])
                x4 = float(row[7])
                y4 = float(row[8])
                point1 = Point(x1, y1)
                point2 = Point(x2, y2)
                point3 = Point(x3, y3)
                point4 = Point(x4, y4)

                # Checking if the house is inside the polygon
                if polygon.contains(point1) and polygon.contains(point2) and polygon.contains(point3) and polygon.contains(point4):
                    finalHouseIDs.append(houseId)
            except Exception as err:
                http_response = make_response(jsonify(
                    {'Error': 'Oops! An error occurred [ERROR]: ' + err}
                ))
                return http_response

    http_response = make_response(jsonify(
        {'HouseId': finalHouseIDs}
    ))
    return http_response

# =====================================================


# debug = True as it was in development mode.
# For production, please remove this parameter
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
