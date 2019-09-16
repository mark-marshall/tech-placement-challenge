errors = {
    'noPricingRules': 'ERROR: An item was passed that has not been included in the pricing rules for UnidaysDiscountChallenge.',
    'noPrice': 'ERROR: An item was passed without a price property.',
    'noStatus': 'ERROR: An item was passed without a status property.',
    'noDiscountFrequency': 'ERROR: A dicountable item was passed without a discountFrequency property.',
    'noDiscountedPrice': 'ERROR: A discountable item was passed without a discountedPrice property.'
}

itemValidatorMap = {
        'allItems': {'price': 'noPrice', 'status': 'noStatus'},
        'Discountable': {'discountFrequency': 'noDiscountFrequency','discountedPrice': 'noDiscountedPrice'}
}

classInjectionMap = {
        'notDiscountable': 'Item',
        'Discountable': 'DiscountableItem'
}
