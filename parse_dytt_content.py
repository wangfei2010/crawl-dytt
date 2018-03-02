# -*- coding: utf-8 -*-
import base64

from bs4 import BeautifulSoup
import threadpool
from common_util import CommonUtils
from headers import headers
from summary_dic import summaryDic
from mongodb_util import MongodbUtils
import logging


class ParseUtil(object):

    def __init__(self):

        self.util = CommonUtils()
        self.pool = threadpool.ThreadPool(10)
        self.mgdb = MongodbUtils()

    def doCallBack(self,requestId,res):
        if res is None:
            return

        try:
            sop = BeautifulSoup(res['text'], "lxml")
            summary = sop.find(id="Zoom").find("td")

            movieInfo = {}
            movieInfo['movieUrl'] = res['url']

            self.__build_movie(movieInfo, summary)
            self.mgdb.save(movieInfo)
        except Exception as e:
            logging.error(e)
            logging.error('Error Get:' + res['url'])
        

    def parse(self, host, content,page):

        tables = content.find_all("table")

        urls = []
        for table in tables:
            tr_title = table.find_all("a")
            
            for tr in tr_title:

                if "index" not in tr.attrs["href"]:
                    #排除电影前面的类型标签
                    m_url = tr.attrs["href"]

                    n_url = host + m_url
                    urls.append({'url':n_url})

        req = threadpool.makeRequests(self.util.doRequest, urls, self.doCallBack)
        map(self.pool.putRequest,req)
        self.pool.wait()
        if page is not None:
            logging.info("完成第%s页解析" % page)

    def __build_movie(self, movieInfo, summary):
        """
        构建电影信息
        :param movieInfo: 电影信息实体 
        :param summary: bs4解析对象
        :return: 
        """
        m_imgs = summary.find_all("img")
        thunder_urls = summary.find_all("a")
        content_array = summary.prettify().replace("<br/>", "\n").split("\n")

        movieInfo['addTime'] = self.util.getTimeNow()

        # 构建图片
        self.__build_images(movieInfo, m_imgs)

        # 构建迅雷地址
        self.__build_thunder_url(movieInfo, thunder_urls)

        # 构建内容
        self.__build_content(movieInfo, content_array)

        # 重建部分内容
        self.__rebuild_content(movieInfo)

    def __containsKey(self, key, dic):
        """
        模糊匹配字典中是否包含该键
        :param key: 查询的键
        :param dic: 字典信息
        :return: 
        """
        t_key = key.replace(" ","").lower()
        for k in dic:
            t_k = k.replace(" ","").lower()
            if t_k in t_key or t_key in t_k:
                return k

        logging.warning('not exist:' + key)
        return None

    def __build_thunder_url(self, movieInfo, thunder_urls):
        """
        构建迅雷地址
        :param movieInfo: 电影信息
        :param thunder_urls: 抓取的迅雷地址
        :return: 
        """
        thunder_url_array = []
        frp_url_array = []
        for url in thunder_urls:
            thunder_url = url.attrs["href"]
            thunder_url_array.append("thunder://" + base64.b64encode("AA" + thunder_url + "ZZ"))
            frp_url_array.append(thunder_url)

        movieInfo['thunderUrl'] = thunder_url_array
        movieInfo['ftpUrl'] = frp_url_array
        movieInfo['_id'] = self.util.getMD5Str(thunder_url_array[0])

    def __build_images(self, movieInfo, m_imgs):
        """
        构建图形信息
        :param movieInfo: 
        :param m_imgs: 
        :return: 
        """
        movie_imgs = []
        for m_img in m_imgs:
            movie_imgs.append(m_img.attrs["src"])
        movieInfo['images'] = movie_imgs

    def __build_content(self, movieInfo, content_array):
        """
        构建内容信息
        :param movieInfo: 
        :param content_array: 
        :return: 
        """
        key = None
        valueArr = []
        for s in content_array:
            s = s.strip(" ")
            if s.startswith("◎"):
                if key is not None:
                    movieInfo[key] = "\n".join(a.strip() for a in valueArr if a != "")
                    valueArr = []
                    key = None
                key = self.__containsKey(s, summaryDic)
                if key is not None:
                    value = s.replace(key, "").replace("\t", "").strip(" ")
                    key = summaryDic[key]
                    valueArr.append(value)
            elif s.startswith("<") is False and s.startswith("◎") is False:
                valueArr.append(s)
            elif s.startswith("<"):
                if key is not None:
                    movieInfo[key] = "\n".join(a.strip() for a in valueArr if a != "")
                    valueArr = []
                    key = None

    def __rebuild_content(self, movieInfo):
        """
        修复部分熟悉
        :param movieInfo: 
        :return: 
        """
        if 'dbScore' in movieInfo.keys():
            dbRecordStr = movieInfo["dbScore"]
            movieInfo["dbScoreStr"] = dbRecordStr

            dbRecord = self.util.getNum(dbRecordStr)
            movieInfo["dbScore"] = dbRecord

        if 'imdbScore' in movieInfo.keys():
            imdbScoreStr = movieInfo["imdbScore"]
            movieInfo["imdbScoreStr"] = imdbScoreStr

            imdbScore = self.util.getNum(imdbScoreStr)
            movieInfo["imdbScore"] = imdbScore
