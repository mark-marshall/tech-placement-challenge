import sys

from config import errors, classInjectionMap, itemValidatorMap

class ErrorLogger:
    def __init__(self, errorMessages, exitCode):
        self.errorMessages = errorMessages
        self.exitCode = exitCode

    # ==== PUBLIC METHODS ====
    def HandleError(self):
        """
        prints each error message and executes the system
        exit.
        """
        for error in self.errorMessages:
            print(errors[error])
        sys.exit(self.exitCode)

class ItemValidator:
    def __init__(self, item, pricingRules):
        self.item = item
        self.pricingRules = pricingRules
        self.itemPricingRules = None
        self.itemInconsistences = []

    # ==== PROTECTED METHODS ====
    def _RunErrorLogger(self):
        """
        Processes any inconsistences through the error logger.
        """
        if len(self.itemInconsistences) > 0:
            errorLog = ErrorLogger(self.itemInconsistences, 0)
            errorLog.HandleError()
    
    def _CheckValidPricingRules(self):
        """
        Checks to see whether an item has the required pricing rules.
        """
        # check keys that need to be included for all items
        for itemValidator in itemValidatorMap['allItems']:
            if itemValidator not in self.itemPricingRules:
                self.itemInconsistences.append(itemValidatorMap['allItems'][itemValidator])
        # check keys that need to be included for this specific item
        if ('status' in self.itemPricingRules) and (self.itemPricingRules['status'] in itemValidatorMap):
            for itemValidator in itemValidatorMap[self.itemPricingRules['status']]:
                if itemValidator not in self.itemPricingRules:
                    self.itemInconsistences.append(itemValidatorMap[self.itemPricingRules['status']][itemValidator])

    # ==== PUBLIC METHODS ====
    def CheckValidity(self):
        """
        Checks to see whether a legitimate item is passed.
        """
        # check whether the item has been included in the pricing rules
        if self.item not in self.pricingRules:
            self.itemInconsistences.append('noPricingRules')
        # check that all relevant information has been included in the pricing rules
        elif self.item in self.pricingRules:
            self.itemPricingRules = self.pricingRules[self.item]
            self._CheckValidPricingRules()
        # process any errors that are found in the checks
        self._RunErrorLogger()

class Item:
    def __init__(self, name, pricingRules):
        self.name = name
        self.quantity = 0
        self.unitPrice = pricingRules['price']
        # the combined cost of all items of this type including discount
        self.totalItemPrice = 0
        # the price change associated with adding an item
        self.priceChange = 0
    
    def __str__(self):
        return f"{self.quantity} x {self.name} = {self.totalItemPrice}"

    # ==== PROTECTED METHODS ====    
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
        Calls the price calculation and returns the price change 
        associated with the added unit.
        """
        self._IncrementQuantity()
        self._CalculatePrice()
        return self.priceChange

class DiscountableItem(Item):
    def __init__(self, name, pricingRules):
        super().__init__(name, pricingRules)
        # number of items required to qualify for a discount
        self.discountFrequency = pricingRules['discountFrequency']
        # price of all items combined in a discount deal
        self.discountedPrice = pricingRules['discountedPrice']
        # number of items that have yet to be included in discounts
        self.discountCounter = 0
    
    # ==== PROTECTED METHODS ====
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

class Basket:
    def __init__(self, pricingRules):
        self.pricingRules = pricingRules
        self.items = {}

    def __str__(self):
        return f"Basket: {self.items}"
    
    # ==== PROTECTED METHODS ====
    def _ItemEligibleForBasket(self,item):
        """
        Checks to see whether the item-type is eligibile to be
        added to the basket and return True in positive cases.
        """
        if item not in self.items:
            return True
    
    # ==== PUBLIC METHODS ====
    def AddItem(self, item):
        """
        Adds the item to the basket.
        """
        # check if this item type is already in the items dict
        if self._ItemEligibleForBasket(item):
            # determine which class the item should be created under
            classToCreate = eval(classInjectionMap[self.pricingRules[item]['status']])
            # create the class for the item
            itemToAdd = classToCreate(item, self.pricingRules[item])
            # add the newly created class to the items dictionary
            self.items[item] = itemToAdd
        # get the price change for adding a unit of the item
        return self.items[item].PriceChange()

class Delivery:
    def __init__(self, deliveryRules):
        # standard delivery charge without discount
        self.standardDeliveryCharge = deliveryRules['standard']
        # value required to qualify for free delivery
        self.freeDeliveryThreshold = deliveryRules['freeThreshold']
    
    # ==== PUBLIC METHODS ====
    def CalculateDeliveryPrice(self, basketPrice):
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
        self.basket = Basket(self.pricingRules)
        self.delivery = Delivery(self.deliveryRules)
        self.price = {
            'Total': 0,
            'DeliveryCharge': 0
        }
    
    # ==== PROTECTED METHODS ====    
    def _UpdateTotalPrice (self,priceChange):
        """
        Updates the total price.
        """
        self.price['Total'] += priceChange

    def _UpdateDeliveryCharge(self, deliveryCharge):
        """
        Updates the delivery charge.
        """
        self.price['DeliveryCharge'] = deliveryCharge
    
    # ==== PUBLIC METHODS ====
    def AddToBasket(self, item):
        """
        Adds the item to the basket and updates charges.
        """
        # check to make sure pricing rules have been provided for the item
        validator = ItemValidator(item, self.pricingRules)
        validator.CheckValidity()
        # add the item to the basket
        priceChange = self.basket.AddItem(item)
        # update the checkout prices
        self._UpdateTotalPrice(priceChange)
        # calculate the delivery price
        deliveryCharge = self.delivery.CalculateDeliveryPrice(self.price['Total'])
        # update the delivery price
        self._UpdateDeliveryCharge(deliveryCharge)
        
    def CalculateTotalPrice(self):
        """
        Returns the current price of the basket and the current delivery 
        charge with all discounts applied.
        """
        return self.price

# TODO: Format output on run_unidays.py and possible API
# TODO: Track total discount
# TODO: STRETCH: Create and deploy Flask APIs
