# -*-coding:UTF-8-*-
import requests
import time
import urllib
import socket

socket.setdefaulttimeout(10);

temp_img_name_list = {}
temp_web_page_name_list = {}


def crawler_resques(url="", ):
    print "request = ", url
    if temp_web_page_name_list.has_key(url):
        return ""
    else:
        temp_web_page_name_list[url] = url
    req_header = {
        'Host': 'cl.abbcl.xyz',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        # 'Proxy-Authorization': 'f23e4ae0cd3a673fad9d510afcd2b9672d0fdcf4186295c455f519bca3150bc248d75ea1ac1bfff3',
        # 'If-Modified-Since': 'Fri, 08 Apr 2016 12:18:39 GMT'

    }
    r = requests.get(url, req_header)
    # print "%%%%%%%%%%%%%%%%%%%%content%%%%%%%%%%%%%%%%%%%%%%%%%"
    # print r.content
    return r.content


def line_has_src_num(line):
    num = 0
    start = 0
    for i in range(100):
        if line.find("src", start):
            num += 1
            start = line.find("src", start) + 3
    return num


def is_down_load_img_file(line):
    if line.find("cdn") != -1 or line.find("jpeg") != -1 or line.find("jpg") != -1:
        return True
    else:
        return False


def is_down_load_gif_file(line):
    if -1 != line.find("gif"):
        return True
    else:
        return False


def etl_content_get_img_url(content=""):
    pass
    content = content.split("\n")
    linenum = 0
    list_img_url = []
    map_img_url = {}
    for line in content:
        if line.find("<img") != -1 or line.find("<input") != -1:
            if line.find("src") == -1:
                continue
            start = 0
            for i in range(line_has_src_num(line)):
                pass
                start = line.find("src=", start)
                end = 0
                if line.find("\'", start + 6) != -1:
                    end = line.find("\'", start + 6)
                else:
                    end = line.find("\"", start + 6)
                # list_img_url.append(line[start+5:end])
                if is_down_load_img_file(line[start + 5:end]):
                    map_img_url[line[start + 5:end]] = line[start + 5:end]
                start = start + 6
                # print "start = ",str(start),"end = ",str(end)
                # print line[start+5:end]
        # print str(linenum), " : ", line
        linenum += 1
    for key in map_img_url:
        list_img_url.append(map_img_url[key])
    print "list_img_utl ", list_img_url
    return list_img_url


def etl_content_get_web_page_url(host="", content=""):
    content = content.split("\n")
    linenum = 0
    list_web_page_url = []
    for line in content:
        if line.find("<a") != -1:
            start = line.find("href=")
            end = line.find("\"", start + 7)
            if line[start + 6:end].find("html") != -1:
                list_web_page_url.append(line[start + 6:end])
                # print "start = ",str(start),"end = ",str(end)
                # print line[start+5:end]
                # print str(linenum), " : ", line
        linenum += 1
    # print list_web_page_url
    return list_web_page_url


def get_host(url):
    lastbackslash = 0
    url.find("/")


def write_file(filename, content):
    ofile = open(filename, "w")
    ofile.write(content)
    ofile.close()


def download_img(url="", path=""):
    try:
        print "download img ", url
        conn = urllib.urlopen(url)
        urlarr = url.split("/")
        img_name = urlarr[len(urlarr) - 1]
        if temp_img_name_list.has_key(img_name):
            return
        else:
            print "save ", img_name
            temp_img_name_list[img_name] = "1"
        f = open(path + urlarr[len(urlarr) - 1], 'wb')
        f.write(conn.read())
        f.close()
    except Exception, e:
        print e.message


if __name__ == '__main__':
    pass
    host = "http://cl.abbcl.xyz/"
    # url = 'http://cl.abbcl.xyz/htm_data/7/1604/1900452.html'
    # content = crawler_resques(url)
    # list_img_url = etl_content_get_img_url(content)
    path = "./cl_img/"
    # for i in list_img_url:
    #     download_img(i,path)
    for page_num in range(2, 500):
        url = "http://cl.abbcl.xyz/thread0806.php?fid=8&search=&page=" + str(page_num)
        list_web_page_url = etl_content_get_web_page_url(host, crawler_resques(url))
        for p in list_web_page_url:
            time.sleep(1)
            content = crawler_resques(host + p)
            list_img_url = etl_content_get_img_url(content)
            for i in list_img_url:
                time.sleep(1)
                download_img(i, path)
                # content = crawler_resques('http://cl.abbcl.xyz/htm_data/8/1604/1900835.html')
                # list_img_url = etl_content_get_img_url(content)
                # num = 0
                # print "len = ",len(list_img_url)
                # for i in list_img_url:
                #     print "----------> ",str(num),"times"
                #     num+=1
                #     time.sleep(1)
                #     download_img(i,path)
