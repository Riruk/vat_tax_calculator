import unittest
from receipt_calculator import ReceiptCalculator

class TestReceiptCalculator(unittest.TestCase):

    def test_init(self):
        calc = ReceiptCalculator()
        self.assertNotEqual(calc.get_product_catalogue(), dict())
        self.assertNotEqual(calc.get_vat_rates(), dict())

    def test_get_price(self):
        calc = ReceiptCalculator()
        self.assertEqual(calc.get_price('Box of Apples'), 1.89)
        self.assertEqual(calc.get_price('Box of Chocolate'), 1.19)

    def test_get_vat(self):
        calc = ReceiptCalculator()
        self.assertEqual(calc.get_vat('Box of Apples'), 4)
        self.assertEqual(calc.get_vat('Box of Ice cream'), 10)
        self.assertEqual(calc.get_vat('Box of Chocolate'), 22)

    def test_full_price(self):
        calc = ReceiptCalculator()
        self.assertEqual(calc.get_full_price('Box of Apples'), 1.89 + 1.89 * 4 / 100)
        self.assertEqual(calc.get_full_price('Box of Ice cream'), 3.29 + 3.29 * 10 / 100)
        self.assertEqual(calc.get_full_price('Box of Chocolate'), 1.19 + 1.19 * 22 / 100)

    def test_set_price(self):
        calc = ReceiptCalculator()
        calc.set_price('Box of Carrots', 1.20)
        self.assertEqual(calc.get_price('Box of Carrots'), 1.20)
        calc.set_price('Bottle of Vine', 'one')  # This addition of a string value should not be allowed
        self.assertIsNone(calc.get_price('Bottle of Vine')) # This assertion should generate error message

    def test_set_vat(self):
        calc = ReceiptCalculator()
        calc.set_vat('Box of Carrots', 4)
        self.assertEqual(calc.get_vat('Box of Carrots'), 4)
        calc.set_vat('Bottle of Vine', 'four') # This addition of a string value should not be allowed
        self.assertEqual(calc.get_vat('Bottle of Vine'), 22) # This assertion should generate error message

if __name__ == '__main__':
    unittest.main()