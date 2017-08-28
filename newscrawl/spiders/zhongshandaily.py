# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class ZhongShanDailySpider(RedisCrawlSpider):
    name = "zhongshandaily"
    allowed_domains = ["zsnews.cn"]
    newspapers = "中山日报"
    redis_key = "zhongshandaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('(part\=\d+)$'))),
        Rule(LinkExtractor(allow=('(article=\d+)$')),callback='parse_item')
    )

    def parse_item(self, response):
        list_title = response.xpath('//td[@id="ContentArea_ArticleTitle_Title"]/text()').extract()
        title = "".join(list_title)
        list_page = response.xpath('//span[@id="ArticlePageHead_thisPage"]/text()').extract()
        page = "".join(list_page)
        list_content = response.xpath('//td[@id="ContentArea_ArticleContent"]/text()').extract()
        content = "".join(list_content)
        list_date = response.xpath('//span[@id="ArticlePageHead_thisPaperDate"]/text()').extract()
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
        list_category = response.xpath('//span[@id="ArticlePageHead_thisNote"]/text()').extract()
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
