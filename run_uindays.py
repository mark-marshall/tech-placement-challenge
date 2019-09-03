from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules

class RunUnidays:
    def __init__(self, checkout, itemsToAdd):
        self.checkout = checkout
        self.itemsToAdd = itemsToAdd
        self.detailedBasket = {}
    
    def AddItems(self):
        """
        Adds all items to the checkout.
        """
        for item in self.itemsToAdd:
            self.checkout.AddToBasket(item)

    def PopulateBasket(self):
        """
        Populates the detailed basket with item information.
        """
        for item in self.checkout.basket.items:
            self.detailedBasket[item] = {
            'quantity': checkout.basket.items[item].quantity,
            'unitPrice': checkout.basket.items[item].unitPrice,
            'finalCost': checkout.basket.items[item].totalItemPrice
            }
    
    def Response(self):
        """
        Combines the final pricing object with detailed basket 
        object.
        """
        res = self.checkout.CalculateTotalPrice()
        res['Basket'] = self.detailedBasket
        return res

    def All(self):
        """
        Runs all required functions to return the checkout response.
        """
        self.AddItems()
        self.PopulateBasket()
        return self.Response()
        
# change the basket here to test different configurations
itemsToAdd = ['A','B','B','C','C','C','D','D','E','E']
# do not alter anything below this line
checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
run = RunUnidays(checkout, itemsToAdd)
print(run.All())
