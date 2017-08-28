# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class HeYuanDailySpider(RedisCrawlSpider):
    name = "heyuandaily"
    allowed_domains = ["heyuan.cn"]
    base_url = "http://epaper.heyuan.cn/"
    newspapers = "河源日报"
    redis_key = "heyuandaily:start_urls"

    def parse_start_url(self, response):
        pages = response.xpath('//*[@id="bmdhTable"]/tbody/tr/td[1]/a')
        for page in pages:
            list_category = page.xpath('text()').extract()
            str_category = "".join(list_category)
            category = str_category.split('：')[1]
            page_path = page.xpath('@href').extract()[0]
            page_index = re.findall('\d{1,}', page_path)
            url = re.sub('(?<=_)\d{1,}',page_index[0],response.url)
            yield Request(url, self.page_parse, dont_filter=True, meta={'category':category})

    def page_parse(self, response):
        articles = response.xpath('//*[@id="main-ed-articlenav-list"]/table/tbody/tr/td[2]/div/a/@href').extract()
        category = response.meta['category']
        for article in articles:
            url = re.sub('(node_\d{1,}\.htm)',article,response.url)
            yield Request(url, self.parse_item, meta={'category':category})

    def parse_item(self, response):
        list_title = response.xpath('//p[@class="BSHARE_TEXT"]/text()').extract()
        title = "".join(list_title)
        list_page = response.xpath('//*[@id="currentBM"]/strong/text()').extract()
        str_page = "".join(list_page)
        page = re.findall('\d{1,}', str_page)[0]
        list_content = response.xpath('//*[@id="ozoom"]/founder-content/text()|//*[@id="ozoom"]/founder-content/p/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
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
