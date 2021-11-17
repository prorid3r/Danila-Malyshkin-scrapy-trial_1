# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from itemloaders.processors import TakeFirst, Compose, Identity
import re

artist_replace_pattern = re.compile(r"^.*:", re.IGNORECASE)
artist_in_title_replace_pattern = re.compile(r" - .*:", re.IGNORECASE)


def get_nested_text(value):
    return ''.join([x.strip() for x in value]).strip()

def strip_author_title(value):
    if value:
        value = [artist_replace_pattern.sub('', x).strip() for x in value[0].split(';')]
    return value

def filter_authors_from_head_title(value):
    if value:
        res = artist_in_title_replace_pattern.search(value)
        if res:
            value = value[:res.span()[0]].strip()
        value = value.replace('-  - SMMAC','').strip()
    return value



class ArtworksItem(scrapy.Item):
    # define the fields for your item here
    url = Field(output_processor=TakeFirst())
    artist = Field(input_processor = Compose(strip_author_title))
    head_title = Field(
        input_processor = Compose(get_nested_text,filter_authors_from_head_title),
        output_processor=TakeFirst())
    title = Field(output_processor=TakeFirst())
    image = Field(output_processor=TakeFirst())
    height = Field(output_processor=TakeFirst())
    width = Field(output_processor=TakeFirst())
    description = Field(
        input_processor = Compose(get_nested_text),
        output_processor=TakeFirst())
    categories = Field(output_processor=Identity())
    pass
