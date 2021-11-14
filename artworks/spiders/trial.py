# -*- coding: utf-8 -*-
import scrapy
# Any additional imports (items, libraries,..)
from artworks.items import ArtworksItem
from scrapy.loader import ItemLoader
import re

class TrialSpider(scrapy.Spider):
    name = 'trial'
    artist_replace_pattern = re.compile(r"^.*:", re.IGNORECASE)
    dimensions_pattern = re.compile(r"[(].*cm[)]")
    float_pattern = re.compile("[+-]?([0-9]*[.])?[0-9]+")

    def start_requests(self):
        urls = [
            'http://pstrial-2019-12-16.toscrape.com/item/15258/Homage_to_Stieglitz?back=146',
        ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_artwork)

    def parse_category(self,response):
        current_category = response.url.split('/')[-1].split('?')[0]
        print(current_category)
        #sub categories
        if not response.meta.get('subcategories_processed'):
            sub_categories = response.xpath("//div[@id='subcats']//a/@href").extract()
            for sub_cat in sub_categories:
                yield response.follow(sub_cat,callback=self.parse_category)
        artwork_links = response.xpath("//div[@id='subcats']/following-sibling::div[1]//a[not(@style = 'visibility: hidden;')]/@href").extract()
        #artworks
        for artwork in artwork_links:
            yield response.follow(artwork,callback=self.parse_artwork,
                                  meta={'categories':response.url.split('browse/')[-1].split('/')})
        #pagination
        if artwork_links:
            url=''
            if '?page=' in response.url:
                tmp = response.url.split('?page=')
                url = f'{tmp[0]}?page={int(tmp[-1])+1}'
                print(url)
            else:
                url = response.url + '?page=1'
            yield response.follow(url, callback=self.parse_category,meta={'subcategories_processed':True})

    def parse_artwork(self,response):
        item = ArtworksItem()
        item['url'] = response.url
        artists = response.xpath("//h2[@class='artist']/text()").extract_first()
        if artists:
            item['artist'] = [self.artist_replace_pattern.sub('', x).strip() for x in artists.split(';')]
        item['title'] = ''.join(response.xpath("//head/title//text()").extract()).strip()
        item['image'] = response.urljoin(response.xpath("//div[@id='body']//img/@src").extract_first())
        item['description'] = ''.join(response.xpath("//div[@class='description']//text()").extract()).strip()
        property_rows = response.xpath("//table[@class='properties']//tr")
        for row in property_rows:
            if row.xpath('.//td[@class="key"]/text()').extract_first() == 'Dimensions':
                dimensions_txt = row.xpath('.//td[@class="value"]/text()').extract_first()
                m = self.dimensions_pattern.search(dimensions_txt)
                if m:
                    dims = [float(x.group()) for x in self.float_pattern.finditer(m.group())]
                    if len(dims)==2:
                        item['height'] = dims[0]
                        item['width'] = dims[1]
        item['categories'] = response.meta.get('categories')
        #item['categories'][-1] = item["categories"][-1].split('?')[0]
        return item










