from flask import Flask, Response, request
from flask_cors import CORS

from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules
from unidays_run import RunUnidays
from config_api import errors, statusCodes

# create Flask app
app = Flask(__name__)
# enable CORS
CORS(app)

# sanity check endpoint
"""
@method: [GET]
@path: '/'
@params: none
@query: none
@body: none
@responses:
    Success (status 200):
    {
        "Mesage": "Server is live."
    }
"""
@app.route('/', methods=['GET'])
def server_check():
    # return success message for sanity check
    return ({'Message': 'Server is live.'}, statusCodes['success'])

# price endpoint
"""
@method: [POST]
@path: '/price'
@params: none
@query: none
@body: {"items": "bbbbccccz"}
@responses: 
    Success (status 200)
    {
        "Basket": {
            "B": {
                "finalCost": 40,
                "itemSavings": 8,
                "quantity": 4,
                "unitPrice": 12
            },
            "C": {
                "finalCost": 14,
                "itemSavings": 2,
                "quantity": 4,
                "unitPrice": 4
            }
        },
        "DeliveryCharge": 0,
        "Errors": {
            "Item Z": [
                {
                    "noPricingRules": "ERROR: An item was passed that has 
                    not been included in the pricing rules."
                }
            ]
        },
        "Savings": 10,
        "Total": 62
    }
    Failure (status 400):
    {
        "Message": "ERROR: An incorrect JSON body was passed with the request. 
        Please provide a JSON body with an items key and list of items e.g. 
        {items: abc}."
    }
"""
@app.route('/price', methods=['POST'])
def calculate_price():
    # save the JSON request body
    itemsSubmitted = request.get_json()
    # check the request contains an items key
    if 'items' not in itemsSubmitted:
        return ({'Message': str(errors['noItemsKey'])}, statusCodes['badRequest'])
    # format the items to a capitalized list
    itemsToAdd = list(str(itemsSubmitted['items']).upper())
    # create a new instance of UnidaysDiscountChallenge
    checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
    # create a new instance of RunUnidays
    run = RunUnidays(checkout, itemsToAdd)
    # return the response from RunUnidays
    return (run.All(), statusCodes['success'])

# serve the app locally on port 5000   
if __name__ == '__main__':
    app.run(port=5000)
