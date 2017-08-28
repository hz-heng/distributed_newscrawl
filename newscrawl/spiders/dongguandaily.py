# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

class DongGuanDailySpider(RedisCrawlSpider):
    name = "dongguandaily"
    allowed_domains = ["timedg.com"]
    base_url = "http://epaper.timedg.com/"
    newspapers = "东莞日报"
    redis_key = "dongguandaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm')),callback='page_parse'),
    )

    def page_parse(self, response):
        articles = response.xpath('/html/body/table/tr[1]/td[1]/table/tr[1]/td/table[2]/tr/td/table/tr[3]/td/table/tr/td[2]/ul/li/a/@href').extract()
        list_page = response.xpath('/html/body/table/tr[1]/td[1]/table/tr[1]/td/table[1]/tr[3]/td[1]/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\w{1,}', str_page, re.A)[0]
        list_category = response.xpath('/html/body/table/tr[1]/td[1]/table/tr[1]/td/table[1]/tr[3]/td[1]/strong/text()').extract()
        category = "".join(list_category)
        for article in articles:
            url = re.sub('node_\d{1,}.htm',article, response.url)
            yield Request(url, self.parse_item, meta={'page':page,'category':category})

    def parse_item(self, response):
        list_title = response.xpath('//td[@class="font01"]/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//*[@id="ozoom"]/span/p/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/','-')
        page = response.meta['page']
        category = response.meta['category']
        if content == "":
            pass
        else:
            item = newsItem()
            item['title'] = title
            item['page'] = page
            item['content'] = content
            item['date'] = date
            item['category'] = category
            item['url'] = response.url
            item['newspapers'] = self.newspapers
            yield item
