from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules
from unidays_run import RunUnidays

itemsToAdd = list(str(input("Type all items to be added here: ")).upper())
    
checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
run = RunUnidays(checkout, itemsToAdd)
print(run.All())
