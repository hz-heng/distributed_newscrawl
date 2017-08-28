# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class JiangMenDailySpider(RedisCrawlSpider):
    name = "jiangmendaily"
    allowed_domains = ["jmrb.com"]
    newspapers = "江门日报"
    redis_key = "jiangmendaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm'),restrict_xpaths=('//*[@id="pageLink"]'))),
        Rule(LinkExtractor(allow=('content_\d+\.htm')),callback='parse_item'),
    )
    
    def parse_item(self, response):
        list_title = response.xpath('/html/body/table/tr[1]/td[2]/table[3]/tr[1]/td/table/tbody/tr/td/strong/text()').extract()
        str_title = "".join(list_title)
        title = str_title.strip()
        list_page = response.xpath('/html/body/table/tr[1]/td[1]/table/tr/td/table[2]/tr/td[1]/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\w{1,}', str_page, re.A)[0]
        list_content = response.xpath('//div[@id="ozoom"]/p/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
        list_category = response.xpath('/html/body/table/tr[1]/td[1]/table/tr/td/table[2]/tr/td[1]/strong/text()').extract()
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
