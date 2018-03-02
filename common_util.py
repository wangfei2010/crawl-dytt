# -*- coding: utf-8 -*-
import datetime
import hashlib
import re
from headers import headers
import requests
from bs4 import BeautifulSoup
import logging

class CommonUtils(object):
    def getMD5Str(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def getTimeNow(self):
        now = datetime.datetime.now()

        return now.strftime('%Y-%m-%d %H:%M:%S')

    def doRequest(self,urlInfo):
        """
        请求访问
        :param urlInfo: 
        :return: 
        """
        url = urlInfo['url']
        logging.info("do Request:" + url)
        host = "http://" + url.split("/")[2]
        response = None

        # 默认超时时间为10s
        timeout = 10
        try:
            response = requests.get(url, headers=headers,timeout=timeout)
            response.encoding = "gbk"
        except Exception as e:
            retry = 5
            while retry > 0:
                logging.warning('尝试重试，重试剩余次数：' + str(retry) + ',url:' + url)
                retry = retry - 1
                try:
                    response = requests.get(url, headers=headers,timeout=timeout)
                    response.encoding = "gbk"
                except Exception as e:
                    logging.error(e)
                else :
                    retry = -1

            if retry == 0:
                logging.error("无法读取数据，URL：" + url)
        
        if response is not None:
            page = None
            if 'page' in urlInfo.keys():
                msg = '开始第%s页解析' % urlInfo['page']
                logging.info(msg)
                page = urlInfo['page']
            return {'text':response.text,'url' : url,'page' : page,'host':host}

    def getNum(self, s):
        pattern = re.compile("^\d\.+\d")
        match = pattern.match(s)
        if match:
            return match.group()

        return 0

    def getTotalCount(self, text):
        """
        获取最大页码数量
        :param text: 
        :return: 
        """
        # 解析数据
        soup = BeautifulSoup(text, "lxml")

        # 获取实际内容
        content = soup.find(class_="co_content8")
        # 获取分页数量
        page_list = list(content.find("select").children)
        return page_list[-2].string
