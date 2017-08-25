# 分布式新闻爬虫（电子报）
* 使用[scrapy-redis](https://github.com/rmax/scrapy-redis)实现分布式爬虫
* 使用[MongoDB](https://www.mongodb.com/)实现持久化存储
## 1、编辑并执行init_redis.py初始化爬取网站URL队列
## 2、使用scrapyd-clients生成egg文件
scrapyd-deploy --build-egg output.egg
## 3、把生成的egg文件放到装有scrapyd的机器上实现分布式爬虫
可以使用[SpiderKeeper](https://github.com/DormyMo/SpiderKeeper)在图形化界面进行管理
