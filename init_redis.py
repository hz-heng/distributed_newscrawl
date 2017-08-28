# -*- coding:utf-8 -*-
import redis
from newscrawl import settings
from datetime import datetime, timedelta
    
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

# -----设置起始时间-----
end = datetime.strptime('2017-08-23', '%Y-%m-%d')
start = datetime.strptime('2017-01-01', '%Y-%m-%d')

d = end - start

for i in range(d.days + 1):
    date = end - timedelta(days=i)
    sdate_1 = date.strftime('%Y%m%d')
    sdate_2 = date.strftime('%Y-%m/%d')
    sdate_3 =date.strftime('%Y-%m-%d')
    sdate_4 =date.strftime('%Y/%m/%d')
    sdate_5 =date.strftime('%Y%m/%d')
    
    url = 'http://epaper.zsnews.cn/zsrb/ShowIndex.asp?paperdate=%s' % sdate_1
    r.lpush('zhongshandaily:start_urls', url)

    url = 'http://strb.dahuawang.com/html/%s/node_24.htm' % sdate_2
    r.lpush('shantoudaily:start_urls', url)

    url = 'http://www.chaozhoudaily.com/czrb/html/%s/node_2.htm' % sdate_2
    r.lpush('chaozhoudaily:start_urls', url)

    url = 'http://epaper.citygf.com/fsrb/html/%s/node_2.htm' %sdate_2
    r.lpush('foshandaily:start_urls', url)

    url = 'http://zhuhaidaily.com.cn/list.php?ud_date=%s' % sdate_3
    r.lpush('zhuhaidaily:start_urls', url)

    url = 'http://www.cnepaper.com/yfrb/html/%s/node_1.htm' % sdate_2
    r.lpush('yunfudaily:start_urls', url)

    url = 'http://yjdaily.yjrb.com.cn/html/%s/node_1.htm' % sdate_2
    r.lpush('yangjiangdaily:start_urls', url)

    url = 'http://xjrb.xjrb.com:8000/epaper/xjrb/%s/pub_index.html' % sdate_4
    r.lpush('xijiangdaily:start_urls', url)

    url = 'http://epaper.qyrb.com:7777/content/%s/PageArticleIndexBT.htm' % sdate_1
    r.lpush('qingyuandaily:start_urls', url)

    url = 'http://mzrb.meizhou.cn/html/%s/node_1.htm' % sdate_2
    r.lpush('meizhoudaily:start_urls', url)

    url = 'http://paper.mm111.net/shtml/mmrb/%s/vlist.shtml' % sdate_1
    r.lpush('maomingdaily:start_urls', url)

    url = 'http://www.jyrb.net.cn/news/index%s.html' % sdate_1
    r.lpush('jieyangdaily:start_urls', url)

    url = 'http://dzb.jmrb.com:8080/jmrb/html/%s/node_22.htm' % sdate_2
    r.lpush('jiangmendaily:start_urls', url)

    url = 'http://e.hznews.com/paper/hzrb/%s/' % sdate_1
    r.lpush('huizhoudaily:start_urls', url)

    url = 'http://sztqb.sznews.com/PC/layout/%s/colA01.html' % sdate_5
    r.lpush('shenzhendaily:start_urls', url)

    url = 'http://szb.sgrb.com/html/%s/node_1.htm' % sdate_2
    r.lpush('shaoguandaily:start_urls', url)

    url = 'http://epaper.timedg.com/html/%s/node_2.htm' % sdate_2
    r.lpush('dongguandaily:start_urls', url)

    url = 'http://epaper.shanweinews.net/content/%s' % sdate_2
    r.lpush('shanweidaily:start_urls', url)

    url = 'http://epaper.heyuan.cn/html/%s/node_1.htm' % sdate_2
    r.lpush('heyuandaily:start_urls', url)

    url = 'http://szb.gdzjdaily.com.cn/zjrb/html/%s/node_2.htm' % sdate_2
    r.lpush('zhanjiangdaily:start_urls', url)

