# coding:utf-8
'''
Created on 2016年8月10日

Get title,keywords,description,class from topics of 163
Algorithm:
function:url_proxies,getHtml,content,title,classification,fun
multithreading

@author: ws
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Queue import Queue
import threading,time
import re,MySQLdb,chardet
import urllib
from random import choice


def url_proxies():
    proxylist = ('211.167.112.14:80',  '210.32.34.115:8080',  '115.47.8.39:80',  '211.151.181.41:80', '219.239.26.23:80')
    proxy = choice(proxylist)
    proxies = {'': proxy}
    opener = urllib.FancyURLopener(proxies)
    # for proxy in proxylist:
    #     proxies = {'': proxy}
    #
    #
    #     print opener
    return opener


def getHtml(i,url):
    try :
        opener = url_proxies()
        page = opener.open(url)
        if page.code == 200 :
            html = page.read()
            # if chardet.detect(html)['encoding'] == 'GB2312':
            html = html.decode('gb2312', 'ignore').encode('utf-8')
            return html
        else:
            return ''
        page.close()

    except Exception,e :
        print i,url
        print e

def content(i, url, html, str_start, str_end):
    # 内容分割的标签

    # content = html.partition(str_start)[2]
    # content = content.partition(str_end)[0]
    try:
        if str_start in html:
            num1 = html.index(str_start, 0)
            # content = content.partition(str_end)[0]
            num2 = html.index(str_end, num1)
            content = html[num1:num2]
        else:
            content = ''
        return content   # 得到网页的内容

    except Exception,e:
        print i,url
        print e


def getTitle(i, url, content, beg=0):
    # 匹配title
    # 思路是利用str.index()和序列的切片
    try:

        if '<title>' in content and '<meta name="keywords" content="' in content and \
                    '<meta name="description" content="' in content and '<meta name="author"' in content:
            num1 = content.index('<title>', beg)+7
            num2 = content.index('</title>', num1)
            title_str = content[num1:num2]
            num3 = content.index('<meta name="keywords" content="', beg)+31
            num4 = content.index('<meta name="description" content="', num3)-4
            keyword_str = content[num3:num4]
            num5 = content.index('<meta name="description" content="', beg) + 34
            num6 = content.index('<meta name="author"', num5) - 4
            description_str = content[num5:num6]
            return title_str,keyword_str,description_str
        else:
            return '','',''

    except Exception,e:
        print i,url
        print e


def classification(i, url, content, beg=0):
    try:
        strlist = re.findall('[\x80-\xff+]+', content)
        str1 = ' '.join(strlist)
        # print chardet.detect(str1)['encoding']
        # cal = str+' '+str1+' '+str2
        return str1

    except Exception, e:
        print i, url
        print e


def connectDatabase(table):
    url_list = []
    try:
        conn = MySQLdb.connect(host='', user='', passwd='', db='', port=3306)
        cur = conn.cursor()

        n = cur.execute('select distinct(f1) from %s order by f1 desc'%table)
        res = cur.fetchall()
        for r in res:
            url_list.append(r[0])
            # print len(r[0])
        cur.close()
        conn.close()
        return url_list
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def fun(table, path1, path2, st):
    url_list = connectDatabase(table)
    cla_list = []
    text_list = []
    f = open(path1, "a+")
    f1 = open(path2, "a+")
    for i in range(st, len(url_list)):#len(url_list)
        t = url_list[i]
        if len(t) < 65 and t[-5:] in ('.html', 'earch'):
            html = getHtml(i,t)
            if html != '':
                content_c = content(i,t,html, '<a href="http://www.163.com/"', '<div')
                if content_c != '' and "网易学院·教程" not in content_c:
                    content_t = content(i,t,html, '<head>', '</head>')
                    if content_t != '' and "404" not in content_t:
                        str1 = classification(i,t,content_c, beg=0)
#                         cla_list.append(str(i) + ':' + str1)
                        title, keyword, description = getTitle(i,t,content_t, beg=0)
#                         text_list.append(title[0]+'\n'+keyword[0]+'\n'+description[0])
                        if str1 != '' and title != '':
                            f.write(str(i) + ':' + str1 + '\n')
    #                         f1 = open(path+"\\%s.txt"%i, "w+")
                            f1.write(str(i) + ':' + title+'\n'+keyword+'\n'+description+'\n'+'\n'+'\n')
                        # f.close()
                            print table + str(time.time())
        time.sleep(1)
    f.close()
    f1.close()


if __name__ == '__main__':
    starttime = time.clock()
    # q = Queue()
    # NUM = 3
    # JOBS = 10
    threads = []
    # t1 = threading.Thread(target=fun,args=('ws_163_tech', "E:\\163\\Tech\\tech.txt", "E:\\163\\Tech\\text.txt", 1000))
    # threads.append(t1)
    t2 = threading.Thread(target=fun,args=('ws_163_money', "E:\\163\\Money\\money.txt",
                                           "E:\\163\\Money\\text.txt", 38594))
    threads.append(t2)
    t3 = threading.Thread(target=fun, args=('ws_163_sports', "E:\\163\\Sports\\sports.txt",
                                            "E:\\163\\Sports\\text.txt", 48346))
    threads.append(t3)
    # t4 = threading.Thread(target=fun, args=('ws_163edu', "E:\\163\\Edu\\edu.txt", "E:\\163\\Edu\\text.txt"))
    # threads.append(t4)
    t5 = threading.Thread(target=fun, args=('ws_163_travel', "E:\\163\\Travel\\travel.txt",
                                            "E:\\163\\Travel\\text.txt", 31826))
    threads.append(t5)
    t7 = threading.Thread(target=fun, args=('ws_163_play', "E:\\163\\Play\\play.txt", \
                                            "E:\\163\\Play\\text.txt", 0))
    threads.append(t7)
    # t8 = threading.Thread(target=fun, args=('ws_163baby', "E:\\163\\Baby\\baby.txt", "E:\\163\\Baby\\text.txt"))
    # threads.append(t8)
    # t9 = threading.Thread(target=fun, args=('ws_163ent', "E:\\163\\Ent\\ent.txt", "E:\\163\\Ent\\text.txt"))
    # threads.append(t9)
    # t10 = threading.Thread(target=fun, args=('ws_163lady', "E:\\163\\Lady\\lady.txt", "E:\\163\\Lady\\text.txt"))
    # threads.append(t10)
    # t11 = threading.Thread(target=fun, args=('ws_163digi', "E:\\163\\Digi\\digi.txt", "E:\\163\\Digi\\text.txt"))
    # threads.append(t11)
    # t12 = threading.Thread(target=fun, args=('ws_163house', "E:\\163\\House\\house.txt", "E:\\163\\House\\text.txt"))
    # threads.append(t12)
    # t13 = threading.Thread(target=fun, args=('ws_163war', "E:\\163\\War\\war.txt", "E:\\163\\War\\text.txt"))
    # threads.append(t13)
    # t14 = threading.Thread(target=fun, args=('ws_163gov', "E:\\163\\Gov\\gov.txt", "E:\\163\\Gov\\text.txt"))
    # threads.append(t14)
    # t15 = threading.Thread(target=fun, args=('ws_163read', "E:\\163\\Read\\read.txt", "E:\\163\\Read\\text.txt"))
    # threads.append(t15)
    # t16 = threading.Thread(target=fun, args=('ws_163health', "E:\\163\\Health\\health.txt", "E:\\163\\Health\\text.txt"))
    # threads.append(t16)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(time.clock()-starttime)