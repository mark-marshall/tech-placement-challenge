pricingRules = {
        'A': {'price': 8, 'status': 'notDiscountable'},
        'B': {'price': 12, 'status': 'Discountable', 'discountFrequency': 2, 'discountedPrice': 20},
        'C': {'price': 4, 'status': 'Discountable', 'discountFrequency': 3, 'discountedPrice': 10},
        'D': {'price': 7, 'status': 'Discountable', 'discountFrequency': 2,'discountedPrice': 7},
        'E': {'price': 5, 'status': 'Discountable', 'discountFrequency': 3,'discountedPrice': 10},
        }

deliveryRules = {
        'standard': 7,
        'freeThreshold': 50
        }

errors = {
    'noPricingRules': 'ERROR: An item was passed that has not been included in the pricing rules for UnidaysDiscountChallenge',
    'noPrice': 'ERROR: An item was passed without a price property',
    'noStatus': 'ERROR: An item was passed witout a status property',
    'noDiscountFrequency': 'ERROR: A dicountable item was passed without a dicountFrequency property',
    'noDiscountedPrice': 'ERROR: A discountable item was passed without a discountedPrice property'
}

itemValidatorMap = {
        'allItems': {'price': 'noPrice', 'status': 'noStatus'},
        'Discountable': {'discountFrequency': 'noDiscountFrequency','discountedPrice': 'noDiscountedPrice'}
}

dependencyInjectionMap = {
        'notDiscountable': '_Item',
        'Discountable': '_DiscountableItem'
}
