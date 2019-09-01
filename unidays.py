import sys

from utils import errors, dependencyInjectionMap

class _Item:
    def __init__(self, name, pricingRules):
        self.name = name
        # unused quantity propery included for future-use
        self.quantity = 0
        self.unitPrice = pricingRules['price']
        # the combined cost of all items of this type including discount
        self.totalItemPrice = 0
        # the price change associated with adding an item
        self.priceChange = 0

    # ==== PRIVATE METHODS ====    
    def _IncrementFullPrice(self):
        """
        Adds the full-price of an item onto the current total price.
        """
        self.totalItemPrice += self.unitPrice
    
    def _CalculatePriceChange(self):
        """
        Updates the price change property with the latest price change 
        after adding a new unit.
        """
        self.priceChange = self.unitPrice

    def _CalculatePrice(self):
        """
        Calls all necessary functions to update the price.
        """
        # increment the price with the full-price of the item
        self._IncrementFullPrice()
        # calculate the final price change after adding the unit
        self._CalculatePriceChange()
    
    def _IncrementQuantity(self):
        """
        Increments the quantity of the item.
        """
        self.quantity += 1

    # ==== PUBLIC METHODS ====
    def PriceChange(self):
        """
        Starts the price calculation and returns the price change
        associated with the added unit.
        """
        self._CalculatePrice()
        return self.priceChange

class _DiscountableItem(_Item):
    def __init__(self, name, pricingRules):
        super().__init__(name, pricingRules)
        # number of items required to qualify for a discount
        self.discountFrequency = pricingRules['discountFrequency']
        # price of all items combined in a discount deal
        self.discountedPrice = pricingRules['discountedPrice']
        # number of items that have yet to be included in discounts
        # stays at 0 if the item has no applicable discount rules
        self.discountCounter = 0
    
    # ==== PRIVATE METHODS ====
    def _ApplyDiscount(self):
        """
        Checks to see if a multi-buy discount can be applied and 
        adjusts the price according to the pricing rules.
        """
        # increment the discount counter for items with potential discounts
        self.discountCounter += 1
        # check to see if the frequency has been reached where discount can be applied
        if self.discountCounter == self.discountFrequency:
            # reset the discount counter to 0
            self.discountCounter = 0
            # remove full prices and replace with the discounted value
            self.totalItemPrice -= (self.unitPrice * self.discountFrequency)
            self.totalItemPrice += self.discountedPrice

    def _CalculatePriceChange(self, previousPrice):
        """
        Updates the price change property with the latest price change 
        after adding a new unit and applying all discounts.
        """
        self.priceChange = self.totalItemPrice - previousPrice
    
    def _CalculatePrice(self):
        """
        Calls all necessary functions to update the price with all 
        applicable discounts.
        """
        # hold the previous price for the price change calculation
        previousPrice = self.totalItemPrice
        # increment the price with the full-price of the item
        self._IncrementFullPrice()
        # check for and apply discounts
        self._ApplyDiscount()
        # calculate the final price change after adding the unit
        self._CalculatePriceChange(previousPrice)

class _Basket:
    def __init__(self, pricingRules):
        self.pricingRules = pricingRules
        self.items = {}
    
    def _ItemInBasketCheck(self,item):
        """
        Checks to see whether this item-type already exists in the basket,
        return True in positive cases.
        """
        if item not in self.items:
            return True
    
    def _AddItem(self, item):
        """
        Adds the item to the basket.
        """
        # check if this item type is already in the items dict
        if self._ItemInBasketCheck(item):
            # determine which class the item should be created under
            classToCreate = eval(dependencyInjectionMap[self.pricingRules[item]['status']])
            # create the class for the item
            itemToAdd = classToCreate(item, self.pricingRules[item])
            # add the newly created class to the items dict
            self.items[item] = itemToAdd
        # get the price change for adding a unit of the item
        return self.items[item].PriceChange()

class _Delivery:
    def __init__(self, deliveryRules):
        self.freeDeliveryThreshold = deliveryRules['freeThreshold']
        self.standardDeliveryCharge = deliveryRules['standard']
    
    def _CalculateDeliveryPrice(self, basketPrice):
        """
        Returns the delivery charge according to the delivery rules.
        """
        if basketPrice >= self.freeDeliveryThreshold:
            return 0
        elif basketPrice < self.freeDeliveryThreshold:
            return self.standardDeliveryCharge
    
class UnidaysDiscountChallenge:
    def __init__(self, pricingRules, deliveryRules):
        self.pricingRules = pricingRules
        self.deliveryRules = deliveryRules
        self.basket = _Basket(self.pricingRules)
        self.delivery = _Delivery(self.deliveryRules)
        self.price = {
            'Total': 0,
            'DeliveryCharge': 0
        }
    
    # ==== PRIVATE METHODS ====
    def _HandleError(self, exitCode, errorMessage):
        """
        Takes an exitCode and an error string and handles the error.
        """
        print(errors[errorMessage])
        sys.exit(exitCode)

    def _CheckItemValidity(self, item):
        """
        Checks to see whether a legitimate item is passed with required
        pricing rules, calls the error handler if otherwise.
        """
        if item not in self.pricingRules:
            self._HandleError(0, 'invalidItem')
    
    def _UpdateTotalPrice (self,priceChange):
        """
        Updates the total price including any discounts.
        """
        self.price['Total'] += priceChange

    def _UpdateDeliveryCharge(self, deliveryCharge):
        """
        Updates the delivery charge according to the delivery rules.
        """
        self.price['DeliveryCharge'] = deliveryCharge
    
    # ==== PUBLIC METHODS ====
    def AddToBasket(self, item):
        """
        Adds the item to the basket and calls the _UpdatePrice function.
        """
        # check to make sure pricing rules have been provided for the item
        self._CheckItemValidity(item)
        # add the item to the basket
        priceChange = self.basket._AddItem(item)
        # update the checkout price
        self._UpdateTotalPrice(priceChange)
        # calculate the delivery price
        deliveryCharge = self.delivery._CalculateDeliveryPrice(self.price['Total'])
        # update the delivery price
        self._UpdateDeliveryCharge(deliveryCharge)
        
    
    def CalculateTotalPrice(self):
        """
        Returns the current price of the basket and the current delivery 
        charge with all discounts are applied.
        """
        return self.price


# TODO: Work through comments and reword
# TODO: Unhappy path when correct discount properties are not included in a discountable item
