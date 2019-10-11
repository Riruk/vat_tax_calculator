import os, csv, re, sys

cur_folder = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(cur_folder, 'data')
INPUT_FOLDER = os.path.join(cur_folder, 'input')
PRODUCT_CATALOGUE_FILE = os.path.join(DATA_FOLDER, 'product_catalogue.csv')
VAT_RATES_FILE = os.path.join(DATA_FOLDER, 'vat_rates.csv')

class ReceiptCalculator:
    def __init__(self, product_catalogue_file=PRODUCT_CATALOGUE_FILE, vat_rates_file=VAT_RATES_FILE):
        self.product_catalogue = dict() #The product catalogue is in the form of {"box of apples": 1.89}
        self.vat_rates = dict() #The vat rates is in the form of {"apples": 4}, where "apple" is the product name part after 'of'
        self.load_catalogue(product_catalogue_file)
        self.load_vats(vat_rates_file)

    def load_catalogue(self, product_catalogue_file):
        # This method loads product_catalogue data from product_catalogue_file
        if not os.path.exists(product_catalogue_file):
            print('I cannot find product catalogue file in {}'.format(product_catalogue_file))
            return

        try:
            with open(product_catalogue_file, 'r', encoding='utf8') as f_in:
                reader = csv.reader(f_in, delimiter=';')
                for line in reader:
                    try:
                        product = line[0].lower().strip()
                        price = line[1]
                        self.product_catalogue[product] = float(price)
                    except Exception as e:
                        print('There occured an error, while I was trying to parse catalogue line: {}'.format(line))
                        print(str(e))
        except OSError as e:
            print('I cannot open product catalogue file {}'.format(product_catalogue_file))
            print(str(e))
        except Exception as e:
            print('An exception occurred, while I was trying to read product catalogue data from {}'.format(product_catalogue_file))
            print(str(e))

    def load_vats(self, vat_rates_file):
        # This method loads vat_rates data from vat_rates_file
        if not os.path.exists(vat_rates_file):
            print('I cannot find product catalogue file in {}'.format(vat_rates_file))
            return

        try:
            with open(vat_rates_file, 'r', encoding='utf8') as f_in:
                reader = csv.reader(f_in, delimiter=';')
                for line in reader:
                    try:
                        vat_rate = line[0]
                        products = re.sub(r'[\[\]"]', '', line[1]).split(',')
                        for product in products:
                            self.vat_rates[product.strip()] = int(vat_rate)
                    except Exception as e:
                        print('There occured an error, while I was trying to parse vat tax line: {}'.format(line))
                        print(str(e))
        except OSError as e:
            print('I cannot open vat tax file {}'.format(vat_rates_file))
            print(str(e))
        except Exception as e:
            print('An exception occurred, while I was trying to read vat tax data from {}'.format(
                vat_rates_file))
            print(str(e))

    def get_product_catalogue(self):
        #This method returns product_catalogue loaded in memory
        return self.product_catalogue

    def get_vat_rates(self):
        #This method returns the vat_rates database loaded in memory
        return self.vat_rates

    def get_price(self, product):
        # This method returns price for a product. In case product is not listed in the product_catalogue, returns None
        try:
            return self.product_catalogue[product.lower()]
        except Exception as e:
            print('I cannot find product {} in the product catalogue'.format(product))
            print(str(e))
            return

    def get_vat(self, product):
        # This method returns vat for the product (in %).
        # In case product is not listed in the vat_rates database, the method assumes vat equal to 22
        search_term = product.lower().split('of')[-1].strip()
        try:
            return self.vat_rates[search_term]
        except Exception as e:
            print('An exception occured, while looking for VAT number for {}, assuming that VAT = 22%'.format(product))
            print(str(e))
            return 22

    def get_full_price(self, product):
        # The method returns the full price of a product (price + price * VAT%)
        # I do not use this method for the task. However, I find it
        price = self.get_price(product)
        vat = self.get_vat(product)
        if price is None or vat is None:
            return
        return price + price * vat / 100

    def set_price(self, product, price):
        # This method sets the price of the product (or adds a new product in the product catalogue)
        # I do not use this method for the task. However, it will be necessary to have it in case of any extensions
        if not isinstance(price, float) and not isinstance(price, int):
            print('I do not update the catalogue with "Product: {}, Price: {}", since price should be of type float'
                  'or int.'.format(product, price))
            return
        self.product_catalogue[product.lower()] = price

    def set_vat(self, product, vat):
        # This method updates product's vat (or updates VAT for already existing product)
        # I do not use this method for the task. However, it will be necessary to have it in case of any extensions
        if not isinstance(vat, float) and not isinstance(vat, int):
            print('I do not update the vat rates database with "Product: {}, VAT: {}", since VAT should be of type int'
                  'or float.'.format(product, vat))
            return
        product = product.lower()
        if 'of' in product:
            product = product.split('of')[-1].strip()
        self.vat_rates[product] = vat

    def process_input_file(self, input_file):
        total = 0
        vat_total = 0
        print('OUTPUT for {}'.format(input_file))
        try:
            with open(input_file, 'r', encoding='utf8') as f_in:
                reader = csv.reader(f_in, delimiter=';')
                for line in reader:
                    try:
                        quantity = int(line[0])
                        product = re.sub(r'[\[\]"]', '', line[1]).strip()
                        price = self.get_price(product)
                        if price is None:
                            print('[SKIPPING] I cannot get price for {}'.format(line))
                            continue
                        vat = price * self.get_vat(product) / 100
                        full_price = (price + vat) * quantity
                        vat_total += vat * quantity
                        total += full_price
                        print('{0:} {1:30} {2:10.2f} €'.format(quantity, product, full_price))
                    except Exception as e:
                        print('There occured an error, while I was trying to process line in input file: {}'.format(line))
                        print(str(e))
                print('-' * 45)
                print('Total {0:>37.2f} €'.format(total))
                print('VAT {0:>39.2f} €'.format(vat_total))
        except OSError as e:
            print('I cannot open input file {}'.format(input_file))
            print(str(e))
        except Exception as e:
            print('An exception occurred, while I was trying to read data from {}'.format(input_file))
            print(str(e))


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        input_file = os.path.join(INPUT_FOLDER, 'input_1.csv')
    else:
        input_file = args[1]
    calculator = ReceiptCalculator()
    calculator.process_input_file(input_file)