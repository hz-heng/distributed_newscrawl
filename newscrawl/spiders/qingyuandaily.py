# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class QingYuanDailySpider(RedisCrawlSpider):
    name = "qingyuandaily"
    allowed_domains = ["qyrb.com"]
    newspapers = "清远日报"
    redis_key = "qingyuandaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('Articel\w+\.htm')),callback='parse_item'),
    )
    
    def parse_item(self, response):
        list_title = response.xpath('//div[@class="detailtitle"]/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//*[@id="contenttext"]/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date[:4] + '-' + str_date[4:6] + '-' + str_date[6:8]
        list_page_category = response.xpath('/html/body/div[1]/table[1]/tbody/tr/td[2]/table[2]/tbody/tr[1]/td/div/strong[1]/font/text()').extract()
        str_page_category = "".join(list_page_category)
        page = re.findall('\w{1,}', str_page_category, re.A)[0]
        category = str_page_category.split(':')[1]
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
