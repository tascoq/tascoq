# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NambafoodItem(scrapy.Item):
    # define the fields for your item here like:
    cafe_name = scrapy.Field()
    cafe_image = scrapy.Field()
    avg_price = scrapy.Field()
    restaurant_categories = scrapy.Field()
    dishes = scrapy.Field()

    pass
