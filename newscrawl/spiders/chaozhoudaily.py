# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class ChaoZhouDailySpider(RedisCrawlSpider):
    name = "chaozhoudaily"
    allowed_domains = ["chaozhoudaily.com"]
    newspapers = "潮州日报"
    redis_key = "chaozhoudaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm'))),
        Rule(LinkExtractor(allow=('content_\d+\.htm')),callback='parse_item')
    )

    def parse_item(self, response):
        list_title = response.xpath('//td[@class="font01"]/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//*[@id="ozoom"]/founder-content/p/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/','-')
        list_page = response.xpath('//*[@id="logoTable"]/tr/td[1]/table/tr[1]/td/table[2]/tr/td[2]/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\w{1,}', str_page, re.A)[0]
        list_category = response.xpath('//*[@id="logoTable"]/tr/td[1]/table/tr[1]/td/table[2]/tr/td[2]/strong/text()').extract()
        category = "".join(list_category)
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
