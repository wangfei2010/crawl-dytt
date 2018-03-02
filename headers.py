# -*- coding: utf-8 -*-
import random

from user_agents import agents

'''
Accept-Encoding:gzip, deflate, sdch
Accept-Language:zh-CN,zh;q=0.8
Cache-Control:max-age=0
Connection:keep-alive
Cookie:__guid=98224921.3307572147961088500.1505044174736.0496; UM_distinctid=15e6b9fa04821c-008c00b1be010e-35465d60-100200-15e6b9fa04923a; 37cs_pidx=2; 37cs_user=37cs24828186416; 37cs_show=31%2C253%2C75; cscpvcouplet_fidx=2; cscpvrich5041_fidx=1; monitor_count=26; CNZZDATA1260535040=1952275212-1505038732-null%7C1505487343
Host:www.dytt8.net
If-Modified-Since:Wed, 13 Sep 2017 15:27:51 GMT
If-None-Match:"807587dca42cd31:2b3"
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
'''

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "If-Modified-Since": "Wed, 13 Sep 2017 15:27:51 GMT",
    "If-None-Match": "80dfa38bc431d31:530",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": "37cs_pidx=2; 37cs_user=37cs64916674987; 37cs_show=253%2C69",
    "User-Agent": agents[random.randint(0, len(agents) - 1)]
}
