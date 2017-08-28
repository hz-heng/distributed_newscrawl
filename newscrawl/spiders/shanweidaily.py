# -*- coding: utf-8 -*-
import re
from newscrawl.items import newsItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class ShanWeiDailySpider(RedisCrawlSpider):
    name = "shanweidaily"
    allowed_domains = ["shanweinews.net"]
    base_url = "http://epaper.shanweinews.net"
    newspapers = "汕尾日报"
    redis_key = "shanweidaily:start_urls"

    def parse_start_url(self, response):
        pages = response.xpath('//*[@id="pagetitleslist"]/ul/li/span[@class="txt"]/a')
        for page in pages:
            page_path = page.xpath('@href').extract()[0]
            url = self.base_url + page_path
            list_category = page.xpath('text()').extract()
            str_category = "".join(list_category)
            page = page_path.split('/')[-1]
            category = str_category.split('：')[1]
            yield Request(url, self.page_parse, dont_filter=True, meta={'page':page,'category':category})

    def page_parse(self, response):
        articles = response.xpath('//*[@id="pagenews"]/ul/li/a/@href').extract()
        page = response.meta['page']
        category = response.meta['category']
        for article in articles:
            url = self.base_url + article
            yield Request(url, self.parse_item, meta={'page': page,'category':category})

    def parse_item(self, response):
        list_title = response.xpath('//*[@class="newsdetail_bg clearfix"]/h1/text()').extract()
        title = "".join(list_title)
        list_content = response.xpath('//*[@class="newsdetail_bg clearfix"]/div[@class="content"]/p/span/text()').extract()
        content = "".join(list_content)
        list_date = re.findall('(?<=/)\d{1,}-\d{1,}/\d{1,}(?=/)', response.url)
        str_date = "".join(list_date)
        date = str_date.replace('/', '-')
        page = response.meta['page']
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
