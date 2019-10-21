# UNiDAYS Discounts Coding Challenge

## Contents
1. [Challenge](#Challenge)
2. [Approach](#Approach)
3. [Instructions](#Instructions)

## Challenge

This challenge is for you to make use of your problem solving skills as well as demonstrate your understanding of good object-oriented programming and SOLID design principles.

At UNiDAYS our business is built on providing discounts to students. Your challenge is to build a basic discount system that applies discounts to an online shopping order and calculates the total price based on a set of pricing rules.

You may complete the challenge in any programming language you wish.

### Pricing Rules

| Item | Price  | Discount |
| ---- | ------ | -------- |
| A    | £8.00  | None |
| B    | £12.00 | 2 for £20.00 |
| C    | £4.00  | 3 for £10.00 |
| D    | £7.00  | Buy 1 get 1 free |
| E    | £5.00  | 3 for the price of 2 |

### Delivery Charges

Delivery charge £7.00

Free delivery on orders over £50.00 (inclusive)

### Interface

Implement a `UnidaysDiscountChallenge` class with two public methods.

1. `AddToBasket` - Pass in an item
2. `CalculateTotalPrice` - Calculate and return the total price, result should include the following
    - `Total` - Total price of all items after applying any discounts
    - `DeliveryCharge` - The delivery charge for the order

## Approach

The design of the solution can roughly be mapped to the following table in which the final output was shaped in some way by 4 key focus areas: (1) users (internal), (2) users (external), (3) testing, and (4) coding for the unhappy path.

| Focus | Description  | Solution | Improvements |
| ----- | ---- | -------- | --------- |
| Users (internal devs)    | Creating a highly readable, maintainable, and configurable program.   | **Readability**: included descriptions for all methods and added comments in any places of potential ambiguity. **Maintainability**: (a) followed single-purpose practises on classes so that they can be easily switched in and out and ammended, (b) deployed the API as a single-purpose server so that any exceptions/errors that arise from this functionality can be readily found and fixed. **Configurability**: removed hardcoding from any of the classes so that any changes required for pricing rules, delivery rules, class injections and error messages are made in centralised locations with one source of truth. | A map/diagram of classes and their relationships would allow devs to quicker understand the structure of the program.  |
| Users (external devs)    | Creating a highly usable and useful program. | **Usability**: made the program accessible as a public API with clear documentation. **Usefulness**: highlighted all information that might be useful to a team creating user interfaces with this information and created a basket object that contains the quantity of all items, savings across each item type, total savings in addition to the total price and delivery cost. | If external teams would in fact have acces to this API, speaking with them to understand the specific use-cases would allow the returned data to be shaped more closely with their business needs. |
| Tests    | Testing the application with all behaviours and edge cases.  | Used the tests provided in the challenge description to test MVP features and then added further tests to (a) test alternative pricing rules, and (b) test STRETCH features such as returning total savings. | MVP tests were written after the first draft of the program were written, these would have been better written in advance to better understand required functionality and edge cases. |
| Unhappy path    | Handling all possible errors and returning useful information. | Identified the most error-prone aspect of using the program as the configuration files that contain pricing and delivery rules. Handled these errors by validating items and associated rules and returning a log of errors to the user showing which item(s) were at fault and which of the 6 rules had been violated. | Pricing and delivery rules could be checked at instantiaion of `UnidaysDiscountChallenge` to highlight config file errors early on. |

## Instructions

1. [Using the public API](#Using-the-public-API)
2. [Running locally](#Running-locally)

### Using the public API
All API requests are made to: https://unidays-discount.herokuapp.com </br>

Requests and reponses are made in JSON to the following endpoints:
1. [Sanity Check](#Sanity-Check)
2. [Price](#Price)

#### Sanity Check
@method: `GET` </br>
@path: `/` </br>
##### Response:
```
Status 200
    {
        "Message":"Server is live."
    }
```

#### Price
@method: `POST` </br>
@path: `/price` </br>
@body: `{"items": "bbbbccccz"}`

##### Response:
```
Status 200
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
```
```
Status 400
    {
        "Message": "ERROR: An incorrect JSON body was passed with the request. 
        Please provide a JSON body with an items key and list of items e.g. 
        {items: abc}."    
    }
```

### Running locally
1. [Setup](#Setup)
2. [Tests](#Tests)
3. [REPL](#REPL)

#### Setup
1. Ensure you have the following installed:
   - Python v3.7 or later: https://www.python.org/downloads/
2. If you have git istalled, `cd` into the directory where you would like the repo to be stored and run `git clone https://github.com/mark-marshall/tech-placement-challenge.git`. Alternatively, download the ZIP.
3. If you have pipenv installed, run `pipenv install` to install all required dependencies from `Pipfile`. Alternatively, run `pip3 install -r requirements.txt` to install all required dependencies from `requirements.txt`.

#### Tests
1. `cd` into the `unidays/` folder.
2. Run `python3 unidays_test.py`.

#### REPL
1. `cd` into the `unidays/` folder.
2. Run `python3 checkout.py`.
