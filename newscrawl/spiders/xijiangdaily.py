# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class XiJiangDailySpider(RedisCrawlSpider):
    name = "xijiangdaily"
    allowed_domains = ["xjrb.com"]
    newspapers = "西江日报"
    redis_key = "xijiangdaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('/\w{3}/\d+\.shtml'))),
        Rule(LinkExtractor(allow=('/story/\d+\.shtml')),callback='parse_item')
    )
    
    def parse_item(self, response):
        list_title = response.xpath('//p[@class="articleTitle"]/text()').extract()
        title = "".join(list_title)
        list_page = response.xpath('//div[@class="leftTitle"]/text()').extract()
        str_page = "".join(list_page)
        page = str_page.split("：")[1]
        list_content = response.xpath('//div[@class="articleContent"]/p/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}/\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
        category = 'null'
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
