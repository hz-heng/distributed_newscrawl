# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class YangJiangDailySpider(RedisCrawlSpider):
    name = "yangjiangdaily"
    allowed_domains = ["yjrb.com.cn"]
    newspapers = "阳江日报"
    redis_key = "yangjiangdaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm'))),
        Rule(LinkExtractor(allow=('content_\w+\.htm')),callback='parse_item')
    )
    
    def parse_item(self, response):
        list_title = response.xpath('//founder-title/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//*[@id="ozoom"]/founder-content/text()|//*[@id="ozoom"]/founder-content/p/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
        list_category = response.xpath('/html/body/table[1]/tr[1]/td[1]/table/tr[1]/td/table[2]/tr/td[1]/strong/text()').extract()
        category = "".join(list_category)
        list_page = response.xpath('/html/body/table[1]/tr[1]/td[1]/table/tr[1]/td/table[2]/tr/td[1]/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\d{1,}', str_page)[0]
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
