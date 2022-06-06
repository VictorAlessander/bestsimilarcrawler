# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class BestSimilarItem(Item):
    title = Field()
    tags = Field()
    year = Field()
