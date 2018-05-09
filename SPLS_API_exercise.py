from flask import request
from flask import jsonify, make_response
from flask import Flask
import datetime
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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
    # This also checks if the value if the value is positive or not
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
