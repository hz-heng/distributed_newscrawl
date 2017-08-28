# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class ZhanJiangDailySpider(RedisCrawlSpider):
    name = "zhanjiangdaily"
    allowed_domains = ["gdzjdaily.com.cn"]
    newspapers = "湛江日报"
    redis_key = "zhanjiangdaily:start_urls"

    rules = (
        Rule(LinkExtractor(allow=('node_\d+\.htm'))),
        Rule(LinkExtractor(allow=('content_\d+\.htm')),callback='parse_item')
    )

    def parse_item(self, response):
        list_title = response.xpath('//div[@class="cont"]/h1/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//*[@id="ozoom"]/content/p/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/','-')
        list_page = response.xpath('//b[@class="fisrt"]/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\w{1,}', str_page, re.A)[0]
        list_category = response.xpath('//b[@class="fisrt"]/strong/text()').extract()
        category = "".join(list_category)
        if content == "":
            pass
        else:
            '''
            item = newsItem()
            item['title'] = title
            item['page'] = page
            item['content'] = content
            item['date'] = date
            item['category'] = category
            item['url'] = response.url
            item['newspapers'] = self.newspapers
            yield item
            '''
            print(title,page,date,category,content)
