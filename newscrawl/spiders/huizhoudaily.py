# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class HuiZhouDailySpider(RedisCrawlSpider):
    name = "huizhoudaily"
    allowed_domains = ["hznews.com"]
    newspapers = "惠州日报"
    redis_key = "huizhoudaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('(/[A-Z]\d+/)$'))),
        Rule(LinkExtractor(allow=('(/\d+/)$')),callback='parse_item')
    )

    def parse_item(self, response):
        list_title = response.xpath('//div[@class="content"]/h2/text()').extract()
        title = "".join(list_title)
        list_page = re.findall('(?<=/)[A-Z]\d{1,}(?=/)', response.url)
        page = "".join(list_page)
        list_content = response.xpath('//div[@class="cnt-main"]/p/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date[:4] + '-' + str_date[4:6] + '-' + str_date[6:8]
        list_category = response.xpath('//div[@class="info"]/span[2]/a/text()').extract()
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
