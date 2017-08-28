# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class ShaoGuanDailySpider(RedisCrawlSpider):
    name = "shaoguandaily"
    allowed_domains = ["sgrb.com"]
    base_url = "http://szb.sgrb.com/"
    newspapers = "韶关日报"
    redis_key = "shaoguandaily:start_urls"

    def parse_start_url(self, response):
        areas = response.xpath('//*[@class="bmml"]/div[2]/div[2]/ol/div/a[1]')
        for area in areas:
            page = area.xpath('@href').extract()[0]
            page_path = re.findall('(?<=_)\w{1,}(?=.htm)', page)
            url = re.sub('(?<=_)\w{1,}(?=.htm)',page_path[0],response.url)
            str_category = area.xpath('text()').extract()[0]
            category = str_category.split('：')[1]
            yield Request(url, self.page_parse, dont_filter=True, meta={'category':category})

    def page_parse(self, response):
        articles = response.xpath('//ol[@id="breakNewsList"]/div/a/@href').extract()
        category = response.meta['category']
        for article in articles:
            url = re.sub('node_\d{1,}.htm',article, response.url)
            yield Request(url, self.parse_item, meta={'category':category})

    def parse_item(self, response):
        list_title = response.xpath('//div[@class="bmnr_con_biaoti"]/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//*[@id="ozoom"]/founder-content/p/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/','-')
        list_page = response.xpath('//div[@class="b_bot"]/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\w{1,}', str_page, re.A)[0]
        category = response.meta['category']
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
