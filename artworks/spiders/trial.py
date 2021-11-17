# -*- coding: utf-8 -*-
import scrapy
# Any additional imports (items, libraries,..)
from artworks.items import ArtworksItem
from scrapy.loader import ItemLoader
import re

class TrialSpider(scrapy.Spider):
    name = 'trial'
    dimensions_pattern = re.compile(r"[(].*cm[)]")
    float_pattern = re.compile("[+-]?([0-9]*[.])?[0-9]+")

    def start_requests(self):
        urls = [
            'http://pstrial-2019-12-16.toscrape.com/browse/summertime',
            'http://pstrial-2019-12-16.toscrape.com/browse/insunsh'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self,response):
        #sub categories
        if not response.meta.get('subcategories_processed'):
            sub_categories = response.xpath("//div[@id='subcats']//a/@href").extract()
            for sub_cat in sub_categories:
                yield response.follow(sub_cat,callback=self.parse_category)
        #artworks
        artwork_links = response.xpath("//div[@id='subcats']/following-sibling::div[1]//a[not(@style = 'visibility: hidden;')]/@href").extract()
        for artwork in artwork_links:
            yield response.follow(artwork,callback=self.parse_artwork,
                                  meta={'categories':response.url.split('browse/')[-1].split('/')})
        #pagination
        if artwork_links:
            url=''
            if '?page=' in response.url:
                tmp = response.url.split('?page=')
                url = f'{tmp[0]}?page={int(tmp[-1])+1}'
            else:
                url = response.url + '?page=1'
            yield response.follow(url, callback=self.parse_category,meta={'subcategories_processed':True})

    def parse_artwork(self,response):
        l = ItemLoader(item=ArtworksItem(), response=response)
        l.add_value('url',response.url)
        l.add_xpath('artist', "//h2[@class='artist']/text()")
        l.add_xpath('head_title',"//head/title//text()")
        l.add_xpath('title',"//div[@id='content']/h1/text()")
        l.add_value('image',response.urljoin(response.xpath("//div[@id='body']//img/@src").extract_first()))
        l.add_xpath('description',"//div[@class='description']//text()")
        property_rows = response.xpath("//table[@class='properties']//tr")
        for row in property_rows:
            if row.xpath('.//td[@class="key"]/text()').extract_first() == 'Dimensions':
                dimensions_txt = row.xpath('.//td[@class="value"]/text()').extract_first()
                m = self.dimensions_pattern.search(dimensions_txt)
                if m:
                    dims = [float(x.group()) for x in self.float_pattern.finditer(m.group())]
                    if len(dims)>=2:
                        l.add_value('height', dims[0])
                        l.add_value('width', dims[1])
        categories = response.meta.get('categories')
        categories[-1] = categories[-1].split('?')[0]
        l.add_value('categories', categories)
        return l.load_item()










