# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class FoShanDailySpider(RedisCrawlSpider):
    name = "foshandaily"
    allowed_domains = ["citygf.com"]
    newspapers = "佛山日报"
    redis_key = "foshandaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm'))),
        Rule(LinkExtractor(allow=('content_\d+\.htm')),callback='parse_item')
    )

    def parse_item(self, response):
        list_title = response.xpath('//div[@class="title1"]/h1/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//div[@class="content"]/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/','-')
        list_page_category = response.xpath('//div[@class="next"]/ul/li[1]/text()').extract()
        str_page_category = "".join(list_page_category)
        page = re.findall('\w{1,}', str_page_category, re.A)[0]
        category = str_page_category.split('：')[1]
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
