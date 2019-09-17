errors = {
    'noPricingRules': 'ERROR: An item was passed that has not been included in the pricing rules.',
    'noPrice': 'ERROR: An item was passed without a price property.',
    'noStatus': 'ERROR: An item was passed without a status property.',
    'noDiscountFrequency': 'ERROR: A dicountable item was passed without a discountFrequency property.',
    'noDiscountedPrice': 'ERROR: A discountable item was passed without a discountedPrice property.',
    'invalidSelection': 'ERROR: You entered an invalid option.'
}

userInputs = {
        'selection': 'Options: [1] Calculate a new price, [2] Exit\nEnter option: ',
        'items': 'Enter items to be added: '
}

itemValidatorMap = {
        'allItems': {'price': 'noPrice', 'status': 'noStatus'},
        'Discountable': {'discountFrequency': 'noDiscountFrequency','discountedPrice': 'noDiscountedPrice'}
}

classInjectionMap = {
        'notDiscountable': 'Item',
        'Discountable': 'DiscountableItem'
}
