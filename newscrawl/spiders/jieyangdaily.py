# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class JieYangDailySpider(RedisCrawlSpider):
    name = "jieyangdaily"
    allowed_domains = ["jyrb.net.cn"]
    newspapers = "揭阳日报"
    redis_key = "jieyangdaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('detail\d+\.html')),callback='parse_item'),
    )

    def parse_item(self, response):
        list_title = response.xpath('//td[@class="jyrb05"]/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//td[@class="jyrb07"]/p/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date[:4] + '-' + str_date[4:6] + '-' + str_date[6:8]
        page = 'null'
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
