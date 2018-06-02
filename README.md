# bilibili_crwal
该爬虫主要基于Scrapy爬取bilibili的用户信息，用户信息主要存在三个url:

1、基本信息url:'https://space.bilibili.com/ajax/member/GetInfo'

2、关注数和粉丝数url:'https://api.bilibili.com/x/relation/stat?vmid='+该用户的uid

3、用户视频的总播放数url:'https://api.bilibili.com/x/space/upstat?mid='+该用户的uid

主要内容在bilibili/spiders/bili

若想提高爬虫速度，可以更改settings，减少延迟并设置ip池

bilibili网站过大，少量数据还是比较容易爬取的，若要爬完建议改用分布式爬虫。
