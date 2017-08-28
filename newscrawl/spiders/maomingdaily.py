# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class MaoMingDailySpider(RedisCrawlSpider):
    name = "maomingdaily"
    allowed_domains = ["mm111.net"]
    newspapers = "茂名日报"
    redis_key = "maomingdaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('/v\w+\.shtml'))),
        Rule(LinkExtractor(allow=('/\d+\.shtml')),callback='parse_item')
    )

    def parse_item(self, response):
        list_title = response.xpath('//*[@id="content"]/div/h1/text()').extract()
        title = "".join(list_title)
        list_content = response.xpath('//*[@id="content_div"]/p/font/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date[:4] + '-' +  str_date[4:6] + '-' + str_date[6:8]
        list_page_category = response.xpath('//*[@id="content"]/div/p[1]/text()[2]').extract()
        str_page_category = "".join(list_page_category)
        list_page = re.findall('\w{1,}', str_page_category, re.A)
        page = "".join(list_page)
        list_category = re.findall('(?<=:).*', str_page_category)
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
