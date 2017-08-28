# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class ShanTouDailySpider(RedisCrawlSpider):
    name = "shantoudaily"
    allowed_domains = ["dahuawang.com"]
    newspapers = "汕头日报"
    redis_key = "shantoudaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm'))),
        Rule(LinkExtractor(allow=('content_\d+\.htm')),callback='parse_item'),
    )

    def parse_item(self, response):
        list_title = response.xpath('//*[@id="logoTable"]/tr/td[2]/table[2]/tr[2]/td/div/table/tr/td/table/tr[1]/td/table/tbody/tr[2]/td/text()').extract()
        title = "".join(list_title)
        list_page = response.xpath('//*[@id="logoTable"]/tr/td[1]/table/tr[1]/td/table[2]/tr/td[2]/text()').extract()
        str_page = "".join(list_page)
        page = str_page.replace('：', '')
        list_content = response.xpath('//*[@id="ozoom"]/founder-content/p/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
        list_category = response.xpath('//*[@id="logoTable"]/tr/td[1]/table/tr[1]/td/table[2]/tr/td[2]/strong/text()').extract()
        str_category = "".join(list_category)
        category = str_category.replace(' ','')
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
