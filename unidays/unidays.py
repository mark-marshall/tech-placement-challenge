from utils import errors, classInjectionMap, itemValidatorMap

class ErrorLogger:
    def __init__(self, errorMessages):
        self._errorMessages = errorMessages

    # ==== PUBLIC METHODS ====
    def HandleError(self):
        """
        Formats all errors into an error log and returns them.
        """
        errorLog = {}
        for error in self._errorMessages:
            errorLog[error] = errors[error]
        return errorLog

class ItemValidator:
    def __init__(self, item, pricingRules):
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
            self.__CheckValidPricingRules()
        # process and return any errors that are found in the checks
        errorTree = self.__RunErrorLogger()
        if errorTree:
            return errorTree

class Item:
    def __init__(self, name, pricingRules):
        self._name = name
        self._quantity = 0
        self._unitPrice = pricingRules['price']
        # the combined cost of all items of this type including discount
        self._totalItemPrice = 0
        # the price change associated with adding an item
        self._priceChange = 0
        # savings associated with this item type
        self._totalItemSavings = 0
        # the savings associated  with adding an item
        self._savingsChange = 0

    # ==== PROTECTED METHODS ====    
    def _IncrementFullPrice(self):
        """
        Adds the full-price of an item onto the current total price.
        """
        self._totalItemPrice += self._unitPrice
    
    def _CalculatePriceChange(self):
        """
        Updates the price change property with the latest price change 
        after adding a new unit.
        """
        self._priceChange = self._unitPrice

    def _CalculatePrice(self):
        """
        Calls all necessary functions to update the price.
        """
        # increment the price with the full-price of the item
        self.__IncrementFullPrice()
        # calculate the final price change after adding the unit
        self.__CalculatePriceChange()
    
    def _IncrementQuantity(self):
        """
        Increments the quantity of the item.
        """
        self._quantity += 1

    # ==== PUBLIC METHODS ====
    def PriceChange(self):
        """
        Calls the price calculation and returns the price change 
        associated with the added unit.
        """
        self.__IncrementQuantity()
        self.__CalculatePrice()
        return {'priceChange': self._priceChange, 'savingsChange': self._savingsChange}

class DiscountableItem(Item):
    def __init__(self, name, pricingRules):
        super().__init__(name, pricingRules)
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
            self._totalItemPrice -= (self._unitPrice * self._discountFrequency)
            self._totalItemPrice += self._discountedPrice
            # update the cumulative savings associated with this item type
            self._totalItemSavings += ((self._unitPrice * self._discountFrequency) - self._discountedPrice)

    def _CalculatePriceChange(self, previousPrice):
        """
        Updates the price change property with the latest price change 
        after adding a new unit and applying all discounts.
        """
        self._priceChange = self._totalItemPrice - previousPrice
    
    def _CalculateSavingsChange(self, previousSavings):
        """
        Updates the savings change property with the latest savings change 
        after adding a new unit.
        """
        self._savingsChange = self._totalItemSavings - previousSavings
    
    def _CalculatePrice(self):
        """
        Calls all necessary functions to update the price with all 
        applicable discounts.
        """
        # hold the previous price for the price change calculation
        previousPrice = self._totalItemPrice
        # hold the previous savings for the savings change calculation
        previousSavings = self._totalItemSavings
        # increment the price with the full-price of the item
        self.__IncrementFullPrice()
        # check for and apply discounts
        self.__ApplyDiscount()
        # calculate the final price change after adding the unit
        self.__CalculatePriceChange(previousPrice)
        # calculate the final saving changes after adding the unit
        self.__CalculateSavingsChange(previousSavings)

class Basket:
    def __init__(self, pricingRules):
        self._pricingRules = pricingRules
        self._items = {}
    
    # ==== PROTECTED METHODS ====
    def _ItemEligibleForBasket(self,item):
        """
        Checks to see whether the item-type is eligibile to be
        added to the basket and return True in positive cases.
        """
        if item not in self._items:
            return True
    
    # ==== PUBLIC METHODS ====
    def AddItem(self, item):
        """
        Adds the item to the basket.
        """
        # check if this item type is already in the items dict
        if self.__ItemEligibleForBasket(item):
            # determine which class the item should be created under
            classToCreate = eval(classInjectionMap[self._pricingRules[item]['status']])
            # create the class for the item
            itemToAdd = classToCreate(item, self._pricingRules[item])
            # add the newly created class to the items dictionary
            self._items[item] = itemToAdd
        # get the price change for adding a unit of the item
        return self._items[item].PriceChange()

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
        self._pricingRules = pricingRules
        self._deliveryRules = deliveryRules
        self._basket = Basket(self._pricingRules)
        self._delivery = Delivery(self._deliveryRules)
        self._price = {
            'Total': 0,
            'Savings': 0,
            'DeliveryCharge': 0
        }
    
    # ==== PROTECTED METHODS ====
    def _UpdateTotalPrice(self,priceChange):
        """
        Updates the total price.
        """
        self._price['Total'] += priceChange
    
    def _UpdateTotalSavings(self, savingsChange):
        """
        Updates the total savings.
        """
        self._price['Savings'] += savingsChange

    def _UpdateDeliveryCharge(self, deliveryCharge):
        """
        Updates the delivery charge.
        """
        self._price['DeliveryCharge'] = deliveryCharge
    
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
            itemAddedRes = self._basket.AddItem(item)
            # update the total price
            self.__UpdateTotalPrice(itemAddedRes['priceChange'])
            # update the savings value
            self.__UpdateTotalSavings(itemAddedRes['savingsChange'])
            # calculate the delivery charge
            deliveryCharge = self._delivery.CalculateDeliveryPrice(self._price['Total'])
            # update the delivery price
            self.__UpdateDeliveryCharge(deliveryCharge)
        
    def CalculateTotalPrice(self):
        """
        Returns the current price of the basket and the current 
        delivery charge with all discounts applied.
        """
        return self._price
