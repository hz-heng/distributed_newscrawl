# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class MeiZhouDailySpider(RedisCrawlSpider):
    name = "meizhoudaily"
    allowed_domains = ["meizhou.cn"]
    newspapers = "梅州日报"
    redis_key = "meizhoudaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm'))),
        Rule(LinkExtractor(allow=('content_\d+\.htm')),callback='parse_item')
    )

    def parse_item(self, response):
        list_title = response.xpath('//div[@class="middle"]/table[1]/tr[4]/td[2]/table[2]/tbody/tr/td/strong/text()').extract()
        title = "".join(list_title)
        list_page = response.xpath('//div[@class="middle"]/table[1]/tr[4]/td[2]/table[1]/tr[1]/td[1]/div/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\d{1,}', str_page)[0]
        list_content = response.xpath('//*[@id="ozoom"]/founder-content/p/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
        list_category = response.xpath('//div[@class="middle"]/table[1]/tr[4]/td[2]/table[1]/tr[1]/td[1]/div/strong/text()').extract()
        str_category = "".join(list_category)
        category = str_category.strip()
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
