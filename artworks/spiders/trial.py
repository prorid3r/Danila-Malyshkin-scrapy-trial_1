# -*- coding: utf-8 -*-
import scrapy
# Any additional imports (items, libraries,..)


class TrialSpider(scrapy.Spider):
    name = 'trial'
    start_urls = []  # put your start urls here

    def parse(self, response):
        # Put your logic to process artworks directory
        pass