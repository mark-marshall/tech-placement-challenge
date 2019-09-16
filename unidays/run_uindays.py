class RunUnidays:
    def __init__(self, checkout, itemsToAdd):
        self.checkout = checkout
        self.itemsToAdd = itemsToAdd
        self.detailedBasket = {}
    
    # ==== PROTECTED METHODS ====
    def _AddItems(self):
        """
        Adds all items to the checkout.
        """
        for item in self.itemsToAdd:
            self.checkout.AddToBasket(item)

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
        object.
        """
        res = self.checkout.CalculateTotalPrice()
        res['Basket'] = self.detailedBasket
        return res

    # ==== PUBLIC METHODS ====
    def All(self):
        """
        Runs all required functions to return the checkout response.
        """
        self._AddItems()
        self._PopulateBasket()
        return self._Response()
