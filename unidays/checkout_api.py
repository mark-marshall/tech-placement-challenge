from flask import Flask, Response, request
from flask_cors import CORS

from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules
from unidays_run import RunUnidays
from config_api import errors

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def server_check():
    return 'Server is running'

@app.route('/price', methods=['POST'])
def calculate_price():
    itemsSubmitted = request.get_json()
    if 'items' not in itemsSubmitted:
        return (errors['noItemsKey'], 400)
    itemsToAdd = list(str(itemsSubmitted['items']).upper())
    checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
    run = RunUnidays(checkout, itemsToAdd)
    return (run.All(), 200)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
