# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from itemloaders.processors import TakeFirst


class ArtworksItem(scrapy.Item):
    # define the fields for your item here
    url = Field()
    artist = Field()
    title = Field(output_processor=TakeFirst())
    image = Field()
    height = Field()
    width = Field()
    description = Field(output_processor=TakeFirst())
    categories = Field()
    pass
