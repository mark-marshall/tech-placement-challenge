from utils import errors, classInjectionMap, itemValidatorMap

class ErrorLogger:
    def __init__(self, errorMessages):
        # ==== PROTECTED PROPERTIES ====
        self._errorMessages = errorMessages
        self._errorLog = {}

    # ==== PUBLIC METHODS ====
    def HandleError(self):
        """
        Formats all errors into an error log and returns them.
        """
        for error in self._errorMessages:
            self._errorLog[error] = errors[error]
        return self._errorLog

class ItemValidator:
    def __init__(self, item, pricingRules):
        # ==== PROTECTED PROPERTIES ====
        self._item = item
        self._pricingRules = pricingRules
        self._itemPricingRules = None
        self._itemInconsistences = []

    # ==== PROTECTED METHODS ====
    def _RunErrorLogger(self):
        """
        Processes any inconsistences through the error logger.
        """
        if len(self._itemInconsistences) > 0:
            errorLog = ErrorLogger(self._itemInconsistences)
            return errorLog.HandleError()
    
    def _CheckValidPricingRules(self):
        """
        Checks to see whether an item has the required pricing rules.
        """
        # check keys that need to be included for all items
        for itemValidator in itemValidatorMap['allItems']:
            if itemValidator not in self._itemPricingRules:
                self._itemInconsistences.append(itemValidatorMap['allItems'][itemValidator])
        # check keys that need to be included for this specific item
        if ('status' in self._itemPricingRules) and (self._itemPricingRules['status'] in itemValidatorMap):
            for itemValidator in itemValidatorMap[self._itemPricingRules['status']]:
                if itemValidator not in self._itemPricingRules:
                    self._itemInconsistences.append(itemValidatorMap[self._itemPricingRules['status']][itemValidator])

    # ==== PUBLIC METHODS ====
    def CheckValidity(self):
        """
        Checks to see whether a legitimate item is passed.
        """
        # check whether the item has been included in the pricing rules
        if self._item not in self._pricingRules:
            self._itemInconsistences.append('noPricingRules')
        # check that all relevant information has been included in the pricing rules
        elif self._item in self._pricingRules:
            self._itemPricingRules = self._pricingRules[self._item]
            self._CheckValidPricingRules()
        # process and return any errors that are found in the checks
        errorTree = self._RunErrorLogger()
        if errorTree:
            return errorTree

class Item:
    def __init__(self, name, pricingRules):
        # ==== PROTECTED PROPERTIES ====
        self._name = name
        self.quantity = 0
        # the combined cost of all items of this type including discount
        self.totalItemPrice = 0
        # savings associated with this item type
        self.totalItemSavings = 0

        # ==== PUBLIC PROPERTIES ====
        self.unitPrice = pricingRules['price']
        # the price change associated with adding an item
        self._priceChange = 0
        # the savings associated  with adding an item
        self._savingsChange = 0

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
        self._priceChange = self.unitPrice

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
        return {'priceChange': self._priceChange, 'savingsChange': self._savingsChange}

class DiscountableItem(Item):
    def __init__(self, name, pricingRules):
        super().__init__(name, pricingRules)
        # ==== PROTECTED PROPERTIES ====
        # number of items required to qualify for a discount
        self._discountFrequency = pricingRules['discountFrequency']
        # price of all items combined in a discount deal
        self._discountedPrice = pricingRules['discountedPrice']
        # number of items that have yet to be included in discounts
        self._discountCounter = 0
    
    # ==== PROTECTED METHODS ====
    def _ApplyDiscount(self):
        """
        Checks to see if a multi-buy discount can be applied and 
        adjusts the price according to the pricing rules.
        """
        # increment the discount counter for items with potential discounts
        self._discountCounter += 1
        # check to see if the frequency has been reached where discount can be applied
        if self._discountCounter == self._discountFrequency:
            # reset the discount counter to 0
            self._discountCounter = 0
            # remove full prices and replace with the discounted value
            self.totalItemPrice -= (self.unitPrice * self._discountFrequency)
            self.totalItemPrice += self._discountedPrice
            # update the cumulative savings associated with this item type
            self.totalItemSavings += ((self.unitPrice * self._discountFrequency) - self._discountedPrice)

    def _CalculatePriceChange(self, previousPrice):
        """
        Updates the price change property with the latest price change 
        after adding a new unit and applying all discounts.
        """
        self._priceChange = self.totalItemPrice - previousPrice
    
    def _CalculateSavingsChange(self, previousSavings):
        """
        Updates the savings change property with the latest savings change 
        after adding a new unit.
        """
        self._savingsChange = self.totalItemSavings - previousSavings
    
    def _CalculatePrice(self):
        """
        Calls all necessary functions to update the price with all 
        applicable discounts.
        """
        # hold the previous price for the price change calculation
        previousPrice = self.totalItemPrice
        # hold the previous savings for the savings change calculation
        previousSavings = self.totalItemSavings
        # increment the price with the full-price of the item
        self._IncrementFullPrice()
        # check for and apply discounts
        self._ApplyDiscount()
        # calculate the final price change after adding the unit
        self._CalculatePriceChange(previousPrice)
        # calculate the final saving changes after adding the unit
        self._CalculateSavingsChange(previousSavings)

class Basket:
    def __init__(self, pricingRules):
        # ==== PROTECTED PROPERTIES ====
        self._pricingRules = pricingRules
        
        # ==== PUBLIC PROPERTIES ====
        self.items = {}
    
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
            classToCreate = eval(classInjectionMap[self._pricingRules[item]['status']])
            # create the class for the item
            itemToAdd = classToCreate(item, self._pricingRules[item])
            # add the newly created class to the items dictionary
            self.items[item] = itemToAdd
        # get the price change for adding a unit of the item
        return self.items[item].PriceChange()

class Delivery:
    def __init__(self, deliveryRules):
        # standard delivery charge without discount
        self._standardDeliveryCharge = deliveryRules['standard']
        # value required to qualify for free delivery
        self._freeDeliveryThreshold = deliveryRules['freeThreshold']
    
    # ==== PUBLIC METHODS ====
    def CalculateDeliveryPrice(self, basketPrice):
        """
        Returns the delivery charge according to the delivery rules.
        """
        if basketPrice >= self._freeDeliveryThreshold:
            return 0
        elif basketPrice < self._freeDeliveryThreshold:
            return self._standardDeliveryCharge
    
class UnidaysDiscountChallenge:
    def __init__(self, pricingRules, deliveryRules):
        # ==== PROTECTED PROPERTIES ====
        self._pricingRules = pricingRules
        self._deliveryRules = deliveryRules
        self._delivery = Delivery(self._deliveryRules)
        
        # ==== PUBLIC PROPERTIES ====
        self.basket = Basket(self._pricingRules)
        self.price = {
            'Total': 0,
            'Savings': 0,
            'DeliveryCharge': 0
        }
    
    # ==== PROTECTED METHODS ====
    def _UpdateTotalPrice(self,priceChange):
        """
        Updates the total price.
        """
        self.price['Total'] += priceChange
    
    def _UpdateTotalSavings(self, savingsChange):
        """
        Updates the total savings.
        """
        self.price['Savings'] += savingsChange

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
        # check to make sure correct rules have been provided for the item
        validator = ItemValidator(item, self._pricingRules)
        validationErrors = validator.CheckValidity()
        # if validation errors are found for the item, return the errors
        if validationErrors:
            return validationErrors
        # continue if no validation errors are found
        elif not validationErrors:
            # add the item to the basket
            itemAddedRes = self.basket.AddItem(item)
            # update the total price
            self._UpdateTotalPrice(itemAddedRes['priceChange'])
            # update the savings value
            self._UpdateTotalSavings(itemAddedRes['savingsChange'])
            # calculate the delivery charge
            deliveryCharge = self._delivery.CalculateDeliveryPrice(self.price['Total'])
            # update the delivery price
            self._UpdateDeliveryCharge(deliveryCharge)
        
    def CalculateTotalPrice(self):
        """
        Returns the current price of the basket, current savings, 
        and the current delivery charge.
        """
        return self.price
