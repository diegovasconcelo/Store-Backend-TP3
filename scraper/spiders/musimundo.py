import json

import scrapy

from scraper.utils import random_stock


class Musimundo(scrapy.Spider):
    name = 'Musimundo'
    base_url = 'https://www.musimundo.com'

    start_urls_path = [
        '/gaming/c/1',
        '/climatizacion/c/2',
        '/audio-tv-video/c/3',
        '/telefonia/c/5',
        '/informatica/c/6',
        '/electrohogar/c/7',
        '/audio-tv-video/accesorios-de-imagen-y-sonido/c/62',
    ]

    def start_requests(self):
        for url in self.start_urls_path:
            url = self.base_url + url
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        products = response.selector.xpath('//div[@data-product]')
        for product in products:

            detail_str = product.xpath('@data-product').get()
            detail_dict = json.loads(detail_str)

            code = detail_dict.get('code')
            name = detail_dict.get('name')
            url = self.base_url + detail_dict.get('url')
            short_description = detail_dict.get('description')
            web_description = detail_dict.get('webDescription')
            category = detail_dict.get('categories', [])[0].get('name')
            subcategory = detail_dict.get('mainCategoryName')
            currency = detail_dict.get('price', {}).get('currencyIso')
            price = detail_dict.get('price', {}).get('value')
            stock = random_stock()
            brand = detail_dict.get('brandInfo', {}).get('name')
            images = detail_dict.get('images', [])
            image_url = next((i.get('url') for i in images if i.get('format') == 'product'), images[0].get('url'))

            yield {
                'code': code,
                'name': name,
                'url': url,
                'short_description': short_description,
                'web_description': web_description,
                'category': category,
                'subcategory': subcategory,
                'currency': currency,
                'price': price,
                'stock': stock,
                'brand': brand,
                'image_url': image_url
            }
