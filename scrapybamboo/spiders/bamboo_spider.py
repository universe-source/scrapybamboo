# coding:utf8
import os
import scrapy

from scrapybamboo.items.bamboo_item import ScrapybambooItem


class UnusebambooSpider(scrapy.Spider):
    name = 'unusebamboo'
    store = 'download'
    allowed_domains = ['unusebamboo.top']
    start_urls = [
        'https://unusebamboo.top',
    ]

    def download(self, response):
        dirname = '{}/{}/'.format(self.store, self.name)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if response.url.endswith('.html'):
            filename = dirname + response.url.split('/')[-2] + '.html'
        else:
            filename = dirname + 'index.html'

        with open(filename, 'wb') as f:
            f.write(response.body)

    def nav_classify(self, response):
        for sel in response.xpath('//ul/li'):
            data = {
                'title': sel.xpath('a/text()').extract(),
                'link': sel.xpath('a/@href').extract(),
                'desc': sel.xpath('text()').extract()
            }
            yield self._create_item(response, data)

    def _create_item(self, response, data):
        item = ScrapybambooItem()
        item['title'] = data.get('title')
        item['link'] = data.get('link')
        item['desc'] = data.get('desc')
        return item

    def parse(self, response):
        # 下载html页面到本地
        self.download(response)
        # 打印封面nav链接
        return self.nav_classify(response)
