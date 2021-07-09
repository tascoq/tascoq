import scrapy
import pprint

from ..items import NambafoodItem

pp = pprint.PrettyPrinter()


class NambaSpider(scrapy.Spider):
    name = "namba"

    start_urls = ['https://nambafood.kg/cafe']

    def parse(self, response):
        all_links = response.css('a.cafe-item::attr(href)').extract()
        urls = ['https://nambafood.kg' + link for link in all_links]

        for url in urls[:5]:
            yield response.follow(url, callback=self.parse)

        items = NambafoodItem()

        cafe_name = response.css('.cafe--name::text')[0].extract().strip()
        cafe_image = response.css('.prev--thumb img').xpath('@src')[0].extract()
        avg_price = response.css('.information--item--description::text')[0].extract()
        restaurant_categories_ = response.css('.tag-list__tag::text').extract()
        restaurant_categories = [rc.strip() for rc in restaurant_categories_]

        spans = response.css('span.section--container')
        category = {}

        for span in spans:
            category_name = span.css('h2.title::text').get().strip()

            card_items = span.css('div.card--item')

            dish_info = {}

            for card_item in card_items:
                dish_image_ = card_item.css('div.card--item--prev img').xpath('@src')
                if dish_image_:
                    dish_image = dish_image_[0].extract()
                dish_title_ = card_item.css('div.card--item--title::text').extract()
                if dish_title_:
                    dish_title = dish_title_[0].strip()
                dish_price_ = card_item.css('div.price::text').extract()
                if dish_price_:
                    dish_price = dish_price_[0].strip() + ' сом'

                dish_info.update(
                    {dish_title:
                         {'price': dish_price,
                          'image': dish_image
                          }
                     }
                )

            category.update({category_name: dish_info})

        items['cafe_name'] = cafe_name
        items['cafe_image'] = cafe_image
        items['avg_price'] = avg_price
        items['restaurant_categories'] = restaurant_categories
        items['dishes'] = category