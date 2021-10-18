# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChefkochItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    rating_count = scrapy.Field()
    rating = scrapy.Field()
    prep_time = scrapy.Field()
    difficulty = scrapy.Field()
    recipe_date = scrapy.Field()
    ingredients = scrapy.Field()
    recipe_text = scrapy.Field()
    recipe_tags = scrapy.Field()
    recipe_url = scrapy.Field()


