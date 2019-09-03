pricingRules = {
        'F': {'price': 15, 'status': 'notDiscountable'},
        'G': {'price': 10, 'status': 'Discountable', 'discountFrequency': 5, 'discountedPrice': 40},
        'H': {'price': 1, 'status': 'Discountable', 'discountFrequency': 30, 'discountedPrice': 20},
        'I': {'price': 7},
        'J': {'price': 5, 'status': 'Discountable', 'discountFrequency': 3},
        }

deliveryRules = {
        'standard': 25,
        'freeThreshold': 45
        }

errors = {
    'noPricingRules': 'ERROR: An item was passed that has not been included in the pricing rules for UnidaysDiscountChallenge',
    'noPrice': 'ERROR: An item was passed without a price property',
    'noStatus': 'ERROR: An item was passed witout a status property',
    'noDiscountFrequency': 'ERROR: A dicountable item was passed without a discountFrequency property',
    'noDiscountedPrice': 'ERROR: A discountable item was passed without a discountedPrice property'
}

itemValidatorMap = {
        'allItems': {'price': 'noPrice', 'status': 'noStatus'},
        'Discountable': {'discountFrequency': 'noDiscountFrequency','discountedPrice': 'noDiscountedPrice'}
}

classInjectionMap = {
        'notDiscountable': 'Item',
        'Discountable': 'DiscountableItem'
}
