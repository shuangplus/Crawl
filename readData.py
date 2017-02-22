# coding:utf-8

'''
@author = not me
'''


import urllib
from bs4 import BeautifulSoup
import urlparse
import time
import urllib2

url = "http://auto.163.com/"
domain = "auto.163.com"
deep = 0
tmp = ""
sites = set()
visited = set()


# local = set()
def get_local_pages(url, domain):
    global deep
    global sites
    global tmp
    repeat_time = 0
    pages = set()

    # 防止url读取卡住
    while True:
        try:
            print "Ready to Open the web!"
            time.sleep(1)
            print "Opening the web", url
            web = urllib2.urlopen(url=url, timeout=3)
            print "Success to Open the web"
            break
        except:
            print "Open Url Failed !!! Repeat"
            time.sleep(1)
            repeat_time = repeat_time + 1
            if repeat_time == 5:
                return

    print "Readint the web ..."
    soup = BeautifulSoup(web.read())
    print "..."
    tags = soup.findAll(name='a')
    for tag in tags:

        # 避免参数传递异常
        try:
            ret = tag['href']
        except:
            print "Maybe not the attr : href"
            continue
        o = urlparse.urlparse(ret)
        """
        #Debug I/O
        for _ret in o:
            if _ret == "":
                 pass
            else:
                 print _ret
        """
        # 处理相对路径url
        if o[0] is "" and o[1] is "":
            print "Fix  Page: " + ret
            url_obj = urlparse.urlparse(web.geturl())
            ret = url_obj[0] + "://" + url_obj[1] + url_obj[2] + ret
            # 保持url的干净
            ret = ret[:8] + ret[8:].replace('//', '/')
            o = urlparse.urlparse(ret)
            # 这里不是太完善，但是可以应付一般情况
            if '../' in o[2]:
                paths = o[2].split('/')
            for i in range(len(paths)):
                if paths[i] == '..':
                    paths[i] = ''
                    if paths[i - 1]:
                        paths[i - 1] = ''
            tmp_path = ''
            for path in paths:
                if path == '':
                    continue
                tmp_path = tmp_path + '/' + path
            ret = ret.replace(o[2], ret_path)
        print "FixedPage: " + ret

    # # 协议处理
    # if 'http' not in o[0]:
    #     print "Bad  Page：" + ret.encode('ascii')
    #     continue
    #
    # # url合理性检验
    # if o[0] is "" and o[1] is not "":
    #     print "Bad  Page: " + ret
    #     continue
    #
    # # 域名检验
    # if domain not in o[1]:
    #     print "Bad  Page: " + ret
    #     continue

    # 整理，输出
    newpage = ret
    if newpage not in sites:
        print "Add New Page: " + newpage
        pages.add(newpage)


    return pages


# dfs算法遍历全站
def dfs(pages):
    # 无法获取新的url说明便利完成，即可结束dfs
    if pages is set():
        return
    global url
    global domain
    global sites
    global visited
    sites = set.union(sites, pages)
    for page in pages:
        if page not in visited:
            print "Visiting", page
            visited.add(page)
            url = page
            pages = get_local_pages(url, domain)
            dfs(pages)

    print "sucess"


pages = get_local_pages(url, domain)
dfs(pages)
for i in sites:
    print i



