# 本代码是有关消息中间件组件的一些使用

##rabbimq
```
import zz_spider
from zz_spider.rabbit_mq.MqDeal import DealRabbitMQ
```
### 使用
```
# -*- coding: utf-8 -*-
# @Time    : 10/14/21 5:38 PM
# @Author  : ZZK
# @File : test_spider.py
# @describe ：
from zz_spider.RabbitMq import DealRabbitMQ

host = xxx
port = xxx
user = xxx
password = xxx
queue_name = xxx
url_port = xxx


def spider(res):
    """
    :param res:
    :return:
    """

    for i in res:
        data =i
        #mongo(data)
        print(i)

mqobeject = DealRabbitMQ(host,user=user,passwd=password,port=port,url_port=url_port)

#spider_main 放置抓取的主要函数
mqobeject.consumer_mq(spider_main=spider,queue_name=queue_name)

#将错误数据写入失败队列中，后缀名必须为_error
mqobeject.send_mq(queue_name='123_error',msg={'1':1})

```

##kafka
```
# 发送
producer = KkProducer(
    bootstrap_servers=bootstrap_servers,
    options_name=options_name,
    try_max_times=try_max_times
    )

params：
    bootstrap_servers 创建连接域名:端口; (例：127.0.0.1:9092)
    options_name 话题名称：topics (例：topic_{flow_id}_{execute_id}_{data_time})
    try_max_times 失败重试最大次数, 默认为 3

test：测试连接 test_send.py

# 接收
```
> 如需帮助请联系 zzk_python@163.com