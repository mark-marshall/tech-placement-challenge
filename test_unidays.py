import unittest
from unidays import UnidaysDiscountChallenge
from config import pricingRules, deliveryRules
from alt_config import pricingRulesAlt, deliveryRulesAlt

class Test(unittest.TestCase):
    def setUp(self):
        self.pricingRules = pricingRules
        self.deliveryRules = deliveryRules
        self.pricingRulesAlt = pricingRulesAlt
        self.deliveryRulesAlt = deliveryRulesAlt 
    
    def test_empty_basket(self):
        """
        Tests 'Total' and 'DeliveryCharge' for empty baskets
        """
        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        self.assertEqual(priceCalculator.price['Total'], 0)
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 0)
    
    def test_invalid_item(self):
        """
        Tests for a sys exit when an invalidItem is passed.
        """
        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        with self.assertRaises(SystemExit) as status:
            priceCalculator.AddToBasket('Z')
        self.assertEqual(status.exception.code, 0)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        with self.assertRaises(SystemExit) as status:
            priceCalculator.AddToBasket('I')
        self.assertEqual(status.exception.code, 0)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        with self.assertRaises(SystemExit) as status:
            priceCalculator.AddToBasket('J')
        self.assertEqual(status.exception.code, 0)

    def test_non_dicounts(self):
        """
        Tests 'Total' for a variety of baskets in which no discounts are applied
        """
        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        priceCalculator.AddToBasket('A')
        self.assertEqual(priceCalculator.price['Total'], 8)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['A','A','A','A']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 32)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        priceCalculator.AddToBasket('B')
        self.assertEqual(priceCalculator.price['Total'], 12)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['E','E']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 10)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        itemsToAdd = ['F','F', 'F']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 45)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        itemsToAdd = ['G','G', 'G', 'G']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 40)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        itemsToAdd = ['H'] * 12
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 12)


    def test_discounts(self):
        """
        Tests 'Total' for a variety of baskets in which discounts are applied
        """
        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['B','B']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 20)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['C','C','C']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 10)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['D','D','D','D','D','D','D','D','D','D','D','D','D','D']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 49)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['E','E','E']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 10)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['E','E','E','E']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 15)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['B','B','B','B','C','C','C']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 50)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['A','B','B','C','C','C','D','D','E','E']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 55)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['E','D','C','B','A','E','D','C','B','C']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 55)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        itemsToAdd = ['G','G','G','G','G']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 40)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        itemsToAdd = ['H'] * 30
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['Total'], 20)

    def test_paid_delivery(self):
        """
        Tests 'DeliveryCharge' for a variety of baskets in which the delivery fee is not waived
        """
        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        priceCalculator.AddToBasket('A')
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 7)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['D','D','D','D','D','D','D','D','D','D','D','D','D','D']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 7)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        priceCalculator.AddToBasket('F')
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 25)

    def test_free_delivery(self):
        """
        Tests 'DeliveryCharge' for a variety of baskets in which the delivery fee is waived
        """
        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['B','B','B','B','C','C','C']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 0)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['A','B','B','C','C','C','D','D','E','E']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 0)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRules,self.deliveryRules)
        itemsToAdd = ['E','D','C','B','A','E','D','C','B','C']
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 0)

        priceCalculator = UnidaysDiscountChallenge(self.pricingRulesAlt,self.deliveryRulesAlt)
        itemsToAdd = ['G'] * 6
        for item in itemsToAdd:
            priceCalculator.AddToBasket(item)
        self.assertEqual(priceCalculator.price['DeliveryCharge'], 0)

if __name__ == '__main__':
    unittest.main()
