from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules
from unidays_run import RunUnidays

# initialize userInput for conditional while loop
userInput = None
# loop starts here
while not userInput == '2':
    # give option for new price calculation or exit
    userInput = str(input("Options: [1] Calculate a new checkout, [2] Exit\nEnter option: "))
    if userInput == '1':
        itemsToAdd = list(str(input("Enter items to be added: ")).upper())
        # create a new instance of UnidaysDiscountChallenge
        checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
        # create a new instance of RunUnidays
        run = RunUnidays(checkout, itemsToAdd)
        # print the response from RunUnidays
        print(run.All())
    