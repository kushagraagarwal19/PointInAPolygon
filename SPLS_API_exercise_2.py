from flask import request
from flask import jsonify, make_response
from flask import Flask

#=====================================================

def estimate_price(house_feat):

    price = 0.0
    price += 75.0*house_feat['GrLivArea']
    price += 54.0*house_feat['TotalBsmtSF']
    price += 51.0*house_feat['GarageArea']
    price += 671.0*(house_feat['YearBuilt'] - 1990)
    
    return price

#=====================================================

app = Flask(__name__)

@app.route('/houseprice', methods=["GET"])
def elements():

    house_data = {}
    house_data['GrLivArea'] = int(request.args.get('GrLivArea'))
    house_data['TotalBsmtSF'] = int(request.args.get('TotalBsmtSF'))
    house_data['GarageArea'] = int(request.args.get('GarageArea'))
    house_data['YearBuilt'] = int(request.args.get('YearBuilt'))
  
    http_response = make_response(jsonify(
        {'HouseFeatures':house_data, 'PriceEstimate':estimate_price(house_data)}
        ))
  
    return http_response

#=====================================================

if __name__ == '__main__':        
    app.run(host='0.0.0.0',port=5000)