# -*- coding: utf-8 -*-

from scrapy.item import Field, Item

"""
Örnek XML:
==========

<products>
    <product>
        <id>8010568</id>
        <title>Armani Jeans Makyaj Çantası 21 x 14 x 3 cm.</title>
        <category>Kadın > Giyim > Sweatshirt</category>
        <description>
            Renk / Desen: Ekru
            Modelin Bilgileri: Boy: 175 cm. Göğüs: 89 cm. Bel: 62 cm. Kalça: 90 cm.
            Ürün Kodu: MS0200-Ekru
        </description>
        <url>https://www.markafoni.com/product/8010568/</url>
        <brand>Her Güne Bir Kombin</brand>
        <expire_timestamp>2014-07-17 06:02:51</expire_timestamp>
        <currency>TL</currency>
        <sizes>
            <size>M</size>
        </sizes>
        <colors>
            <color>Ekru</color>
        </colors>
        <images>
            <image>https://media.markafoni.com/uploads/cache-r14071001/product/productmeta/2014/07/12/8010568/web_detail/medium/d1be4c5683e34_0_304x424.jpg</image>
            <image>https://media.markafoni.com/uploads/cache-r14071001/product/productmeta/2014/07/12/8010568/web_detail/medium/d1be4c5683e34_1_304x424.jpg</image>
            <image>https://media.markafoni.com/uploads/cache-r14071001/product/productmeta/2014/07/12/8010568/web_detail/medium/d1be4c5683e34_2_304x424.jpg</image>
        </images>
        <special_price>53,99</special_price>
        <price>19,99</price>
    </product>
</products>
"""


class CrawlingItem(Item):
    id = Field()
    url = Field()
    category = Field()
    title = Field()
    priceOld = Field()
    priceNew = Field()
    brand = Field()
    images = Field()
    description = Field()


class ProductItem(Item):
    id = Field()
    title = Field()
    description = Field()
    category = Field()
    url = Field()
    brand = Field()
    expire_timestamp = Field()
    sizes = Field()
    currency = Field()
    colors = Field()
    images = Field()
    price = Field()
    special_price = Field()

