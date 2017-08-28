# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class ZhuHaiDailySpider(RedisCrawlSpider):
    name = "zhuhaidaily"
    allowed_domains = ["zhuhaidaily.com.cn"]
    newspapers = "珠海特区报"
    redis_key = "zhuhaidaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('text\.php\?.*')),callback='parse_item'),
    )

    def parse_item(self, response):
        list_title = response.xpath('//div[@id="main"]/h1/text()').extract()
        title = "".join(list_title)
        list_content = response.xpath('//div[@id="main"]/p/text()').extract()
        content = "".join(list_content)
        date = re.findall('\d{1,}-\d{1,}-\d{1,}', response.url)[0]
        list_page = response.xpath('//div[@id="main"]/div/ul/li[1]/a/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\w{1,}', str_page, re.A)[0]
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
