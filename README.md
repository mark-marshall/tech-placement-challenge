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

## Instructions

1. [Using the public API](#Using-the-public-API)
2. [Running locally](#Running-locally)

### Using the public API
All API requests are made to: https://unidays-discount.herokuapp.com. The following endpoints are available:
1. [Sanity Check](#Sanity-Check)
2. [Price](#Price)

#### Sanity Check
##### Request:
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
##### Request:
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

#### Tests

#### REPL
