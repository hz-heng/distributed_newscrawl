# 分布式新闻爬虫（电子报）
* 使用[scrapy-redis](https://github.com/rmax/scrapy-redis)实现分布式爬虫
* 使用[MongoDB](https://www.mongodb.com/)实现持久化存储
## 1、编辑并执行init_redis.py初始化爬取网站URL队列
对end,start进行修改，设置爬取报纸的天数  
end = datetime.strptime('2017-08-23', '%Y-%m-%d')  
start = datetime.strptime('2017-01-01', '%Y-%m-%d')  
## 2、在settings.py设置数据库连接信息
#MONGODB SETTING  
MONGODB_SERVER = ''  
MONGODB_USER = ''  
MONGODB_PASSWORD = ''  
MONGODB_PORT = 27017  
MONGODB_DB = ''  
MONGODB_COLLECTION = ''  

#REDIS SETTING  
SCHEDULER = "scrapy_redis.scheduler.Scheduler" #从redis读取队列进行调度  
SCHEDULER_PERSIST = True #调度状态持久化(实现暂停/启动爬虫)  
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  
REDIS_HOST = ''  
REDIS_PORT = 6379  
## 3、使用scrapyd-clients生成egg文件
scrapyd-deploy --build-egg output.egg
## 4、把生成的egg文件放到装有scrapyd的机器上实现分布式爬虫
可以使用[SpiderKeeper](https://github.com/DormyMo/SpiderKeeper)在图形化界面进行管理
