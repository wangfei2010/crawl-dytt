# -*- coding: utf-8 -*-
import sys

import requests
import threadpool
from bs4 import BeautifulSoup

from common_util import CommonUtils
from headers import headers

from parse_dytt_content import ParseUtil
import logging

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='log/crawl.log',  
                    filemode='a')

reload(sys)
sys.setdefaultencoding("utf-8")


util = CommonUtils()
pool = threadpool.ThreadPool(10)
parse = ParseUtil()

def callback(requestId, res):

    if res is None:
        return

    # 解析数据
    soup = BeautifulSoup(res['text'], "lxml")

    # 获取实际内容
    content = soup.find(class_="co_content8")

    # 调用解析
    page = None
    if 'page' in res.keys():
        page = res['page']
    parse.parse(res['host'], content,page)


def getMovie(format_url,first=1):
    """
    format : "/html/gndy/dyzz/list_23_%s.html"
    """
    t_url = format_url % first

    # 获取页码
    response = util.doRequest({'url':t_url})
    if response is None:
        logging.error("无法获取第一页数据,url:" + t_url)
        return
    pages = util.getTotalCount(response['text'])
    #pages = 1
    # 构建访问地址
    urls = [{'url':format_url % page,'page':page} for page in range(1, int(pages) + 1)]

    logging.info("共%s页" % pages)
    # 构建线程池访问
    req = threadpool.makeRequests(util.doRequest, urls, callback)
    map(pool.putRequest,req)
    pool.wait()
    logging.info("完成数据抓取")

def build_url_info(url,page=1):
    arr = url.split("/")
    host = "http://" + arr[2]
    html = arr[3]#html
    url_type = arr[4]#gndy or jzyy
    movie_type = arr[5]#oumei or china
    page_url = arr[6]

    url = host + "/" + html + "/" + movie_type + "/" + page_url

    url_info = {
        'url' : url % page,
        'page' : page,
        'host' : host,
        'html' : html,
        'url_type' : url_type,
        'movie_type' : movie_type,
        'page_url' : page_url % page
    }

    return url_info






def getMovieByType(host,video_type,movie_type,page_url_format):
    url = host + "/html/" + video_type + "/" + movie_type + "/" + page_url_format
    getMovie(url)


# 获取最新电影
def getNewMovie(host):
    #http://www.ygdy8.net/html/gndy/dyzz/list_23_2.html
    getMovieByType(host,"gndy","dyzz","list_23_%s.html")

# 获取欧美电影
def getOuMeiMovie(host):
    getMovieByType(host,"gndy","oumei","list_7_%s.html")

# 获取国内电影
def getChinaMovie(host):
    getMovieByType(host,"gndy","china","list_4_%s.html")

# 获取综合电影
def getZongHeMovie(host):
    getMovieByType(host,"gndy","jddy","list_63_%s.html")

# 获取日韩电影
def getRiHanMovie(host):
    getMovieByType(host,"gndy","rihan","list_6_%s.html")

def main():
    host = "http://www.ygdy8.net"
    #getOuMeiMovie(host)
    #getChinaMovie(host)
    #getZongHeMovie(host)
    getRiHanMovie(host)

if __name__ == '__main__':
    main()
