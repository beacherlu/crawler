# -*-coding:UTF-8-*-

import urllib
import itertools
import datetime
import threading
import time
import random
import urllib2
import cookielib
import codecs
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 总共16位数，10^16次方完全可以覆盖
# 每个线程跑20分钟 10000次
TOTALCASENUM = 10000000000000000
EVERYTHREADSCANTIMES = 10000
THREADNUM = TOTALCASENUM / EVERYTHREADSCANTIMES
INTERNAL = EVERYTHREADSCANTIMES


def scan(start=0):
    SUCCESSTIMES = 0
    TOTALTIMES = 0
    starttime = datetime.datetime.now()
    for i in itertools.count(start):
        # print "i=",i
        TOTALTIMES += 1
        try:
            html_src = urllib.urlopen(
                'http://cnkicheck5.cnkifenjie.checkpass.net/call/call.php?do=getReportsByTid&tid=' + str(i)).read()
        except:
            time.sleep(random.randint(1, 120));
            html_src = urllib.urlopen(
                'http://cnkicheck5.cnkifenjie.checkpass.net/call/call.php?do=getReportsByTid&tid=' + str(i)).read()
        if html_src.find("origin_path") != -1:
            # print "Success"
            SUCCESSTIMES += 1
            print "SUCCESS_ID:" + str(i)
            if SUCCESSTIMES > 1000000:
                break
        else:
            print "None_ID:" + str(i)
            # pass
        if TOTALTIMES % 1000000 == 0:
            endtime = datetime.datetime.now()
            print "Seconds:" + str((endtime - starttime).seconds)
            break
    print "TOTAL = " + str(TOTALTIMES)
    print "SUCCESS = " + str(SUCCESSTIMES)


def call_scan():
    threads = []
    for i in itertools.count(1):
        threads.append(threading.Thread(target=scan, args=(i * 100000000 + 1000000000000000,)))
        if i % 10000 == 0:
            break;
    for t in threads:
        t.setDaemon(False)
        t.start()

    print "all over %s" % time.ctime()


def test_scan():
    try:
        html_src = urllib.urlopen('http://caoliushequ.org/').read()
        html_split = html_src.split("\n");
        line_num=0
        ifile=open("out_1.html","w")
        ifile.write(html_src)
        ifile.close();
        for i in html_split:
            #if i.find("<a") !=-1:
            print str(line_num)," : ",i
            line_num+=1
    except:
        print "asdfasfd"


def test_cookies():
    pass;
    url='http://cl.abbcl.xyz/thread0806.php?fid=20'
    req_header = {
#'Host': 'cl.abbcl.xyz',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
#'Proxy-Authorization': 'f23e4ae0cd3a673fad9d510afcd2b9672d0fdcf4186295c455f519bca3150bc248d75ea1ac1bfff3',
#'If-Modified-Since': 'Fri, 08 Apr 2016 12:18:39 GMT'

    }
    req_timeout = 5
    req = urllib2.Request(url,None,req_header)
    resp = urllib2.urlopen(req,None,req_timeout)
    html = resp.read()
    ifile=open("out.html","w")
    ifile.write(html)
    ifile.close();
    #print html.decode('ascii').encode('utf-8')
    #print chardet.detect(html)


if __name__ == '__main__':
    test_cookies()
    #test_scan()
