class RunUnidays:
    def __init__(self, checkout, itemsToAdd):
        self.checkout = checkout
        self.itemsToAdd = itemsToAdd
        self.detailedBasket = {}
        self.errors = {}
    
    # ==== PROTECTED METHODS ====
    def _HandleError(self, item, itemErrors):
        """
        Adds all errors to the errors dictionary.
        """
        if item not in self.errors:
            self.errors[item] = itemErrors

    def _AddItems(self):
        """
        Adds all items to the checkout.
        """
        for item in self.itemsToAdd:
            itemErrors = self.checkout.AddToBasket(item)
            if itemErrors:
                self._HandleError(item, itemErrors)

    def _PopulateBasket(self):
        """
        Populates the detailed basket with item information.
        """
        for item in self.checkout.basket.items:
            self.detailedBasket[item] = {
            'quantity': self.checkout.basket.items[item].quantity,
            'unitPrice': self.checkout.basket.items[item].unitPrice,
            'itemSavings': self.checkout.basket.items[item].totalItemSavings,
            'finalCost': self.checkout.basket.items[item].totalItemPrice
            }
    
    def _Response(self):
        """
        Combines the final pricing object with detailed basket 
        object and any errors.
        """
        res = self.checkout.CalculateTotalPrice()
        res['Basket'] = self.detailedBasket
        if len(self.errors) > 0:
            res['Errors'] = self.errors
        return res

    # ==== PUBLIC METHODS ====
    def All(self):
        """
        Runs all required functions to return the checkout response.
        """
        self._AddItems()
        self._PopulateBasket()
        return self._Response()
