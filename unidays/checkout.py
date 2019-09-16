from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules
from unidays_run import RunUnidays

itemsToAdd = list(str(input("Type all items to be added here: ")).upper())

# create a new instance of UnidaysDiscountChallenge
checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
# create a new instance of RunUnidays
run = RunUnidays(checkout, itemsToAdd)
# print the response from RunUnidays
print(run.All())
