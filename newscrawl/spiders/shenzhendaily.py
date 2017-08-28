# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class ShenZhenDailySpider(RedisCrawlSpider):
    name = "shenzhendaily"
    allowed_domains = ["sznews.com"]
    base_url = "http://sztqb.sznews.com/"
    newspapers = "深圳特区报"
    redis_key = "shenzhendaily:start_urls"
    
    def parse_start_url(self, response):
        areas = response.xpath('//div[@class="Chunkiconlist"]/p/a[1]')
        for area in areas:
            page = area.xpath('@href').extract()[0]
            url = re.sub('\w{1,}.html',page,response.url)
            str_category = area.xpath('text()').extract()[0]
            category = str_category.split('：')[1]
            yield Request(url, self.page_parse, dont_filter=True, meta={'category':category})

    def page_parse(self, response):
        articles = response.xpath('//div[@class="newslist"]/ul/li/h3/a/@href').extract()
        category = response.meta['category']
        for article in articles:
            article_path = re.findall('/\w{1,}/\w{1,}/\w{1,}/\w{1,}.html', article)[0]
            url = self.base_url + 'PC' + article_path
            yield Request(url, self.parse_item, meta={'category':category})

    def parse_item(self, response):
        list_title = response.xpath('//div[@class="newsdetatit"]/h3/text()').extract()
        title = "".join(list_title).strip()
        list_content = response.xpath('//div[@class="newsdetatext"]/founder-content/p/text()').extract()
        content = "".join(list_content).strip()
        list_date = re.findall('(?<=/)\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        n_date = str_date.replace('/','-')
        date = n_date[:4] + '-' + n_date[4:]
        list_page = response.xpath('//div[@class="newsdetatit"]/p[3]/span[@class="Author"]/text()').extract()
        str_page = "".join(list_page)
        page = str_page.split('：')[1]
        if content == "":
            pass
        else:
            item = newsItem()
            item['title'] = title
            item['page'] = page
            item['content'] = content
            item['date'] = date
            item['category'] = response.meta['category']
            item['url'] = response.url
            item['newspapers'] = self.newspapers
            yield item
