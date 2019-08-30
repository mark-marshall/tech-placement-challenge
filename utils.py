pricingRules = {
        'A': {'price': 8, 'isDiscountable': False},
        'B': {'price': 12, 'isDiscountable': True, 'discountFrequency': 2, 'discountedPrice': 20},
        'C': {'price': 4, 'isDiscountable': True, 'discountFrequency': 3, 'discountedPrice': 10},
        'D': {'price': 7, 'isDiscountable': True, 'discountFrequency': 2,'discountedPrice': 7},
        'E': {'price': 5, 'isDiscountable': True, 'discountFrequency': 3,'discountedPrice': 10},
        }

deliveryRules = {
        'standard': 7,
        'freeThreshold': 50
        }

errors = {
    'invalidItem': 'An item was passed that has not been included in the pricing rules for this basket'
}
