class RunUnidays:
    def __init__(self, checkout, itemsToAdd):
        # ==== PROTECTED PROPERTIES ====
        self._checkout = checkout
        self._itemsToAdd = itemsToAdd
        self._detailedBasket = {}
        self._errors = {}
    
    # ==== PROTECTED METHODS ====
    def _HandleError(self, item, itemErrors):
        """
        Adds all errors to the errors dictionary.
        """
        if item not in self._errors:
            self._errors[item] = itemErrors

    def _AddItems(self):
        """
        Adds all items to the checkout.
        """
        for item in self._itemsToAdd:
            itemErrors = self._checkout.AddToBasket(item)
            if itemErrors:
                self._HandleError(item, itemErrors)

    def _PopulateBasket(self):
        """
        Populates the detailed basket with item information.
        """
        for item in self._checkout.basket.items:
            self._detailedBasket[item] = {
            'quantity': self._checkout.basket.items[item].quantity,
            'unitPrice': self._checkout.basket.items[item].unitPrice,
            'itemSavings': self._checkout.basket.items[item].totalItemSavings,
            'finalCost': self._checkout.basket.items[item].totalItemPrice
            }
    
    def _Response(self):
        """
        Combines the final pricing object with detailed basket 
        object and any errors.
        """
        res = self._checkout.CalculateTotalPrice()
        res['Basket'] = self._detailedBasket
        if len(self._errors) > 0:
            res['Errors'] = self._errors
        return res

    # ==== PUBLIC METHODS ====
    def All(self):
        """
        Runs all required functions to return the checkout.
        """
        self._AddItems()
        self._PopulateBasket()
        return self._Response()
