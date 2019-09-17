from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules
from unidays_run import RunUnidays

# initialize userInput
userInput = None
# loop start
while not userInput == '2':
    # provide user option for new price calculation or exit
    userInput = str(input("Options: [1] Calculate a new price, [2] Exit\nEnter option: "))
    # check that the user gave a valid input
    if not (userInput == '1' or userInput == '2'):
        print("ERROR: You entered an invalid option.")
    # check if user selected new price calculation
    elif userInput == '1':
        itemsToAdd = list(str(input("Enter items to be added: ")).upper())
        # create a new instance of UnidaysDiscountChallenge
        checkout = UnidaysDiscountChallenge(pricingRules,deliveryRules)
        # create a new instance of RunUnidays
        run = RunUnidays(checkout, itemsToAdd)
        # print the response from RunUnidays
        print(run.All())
     