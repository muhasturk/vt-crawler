# -*- coding: utf-8 -*-

from lxml import etree
import  re

class DictToXml(object):

    def __init__(self):
        self.products = etree.Element("products")

    @staticmethod
    def convert_value(value):
        if not isinstance(value, unicode):
            value = unicode(value)
        return value

    def add_product(self, data, product_id=0):
        new_product = etree.SubElement(self.products, 'product', id=str(product_id))

        # product properties
        for key, value in data.items():
            if not isinstance(value, list):
                new_property = etree.SubElement(new_product, key)
                new_property.text = self.convert_value(value)
            else:
                new_list = etree.SubElement(new_product, key)
                for sub_value in value:

                    new_sub_elem = etree.SubElement(new_list, key[0:-1])
                    new_sub_elem.text = self.convert_value(sub_value)

    def dump(self):
        return etree.tostring(self.products, pretty_print=True, encoding='utf-8')

def removeCurrency(string):
    return string.replace(getCurrency(string),'').strip()

def getCurrency(string):
    return re.compile("[\d,]*\s*([a-zA-Z]+)").findall(string.strip())[0]

def replaceCommaWithDot(string):
    return string.replace(',','.').strip()


