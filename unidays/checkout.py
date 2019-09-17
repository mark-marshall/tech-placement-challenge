from unidays.unidays_discount import UnidaysDiscountChallenge
from unidays.config import pricingRules, deliveryRules
from unidays.unidays_run import RunUnidays
from unidays.utils import userInputs, errors

# initialize userInput
userInput = None
# loop start
while not userInput == '2':
    # provide user option for new price calculation or exit
    userInput = str(input(userInputs['selection']))
    # check that the user gave a valid input
    if not (userInput == '1' or userInput == '2'):
        print(errors['invalidSelection'])
    # check if user selected new price calculation
    elif userInput == '1':
        itemsToAdd = list(str(input(userInputs['items'])).upper())
        # create a new instance of UnidaysDiscountChallenge
        checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
        # create a new instance of RunUnidays
        run = RunUnidays(checkout, itemsToAdd)
        # print the response from RunUnidays
        print(run.All())
     