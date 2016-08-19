# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')



import re,MySQLdb,chardet
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    if chardet.detect(html)['encoding'] == 'GB2312':
        html = html.decode('gb2312', 'ignore').encode('utf-8')
        return html
    else:
        return ''


def content(html,str_start,str_end):
    # 内容分割的标签

    # content = html.partition(str_start)[2]
    # content = content.partition(str_end)[0]
    if str_start in html:
        num1 = html.index(str_start, 0)
        # content = content.partition(str_end)[0]
        num2 = html.index(str_end, num1)
        content = html[num1:num2]
    else:
        content = ''
    return content   # 得到网页的内容


def title_16(content,beg = 0):
    # 匹配title
    # 思路是利用str.index()和序列的切片

    title_list = []
    keyword_list = []
    description_list = []

    num1 = content.index('<title>', beg)+7
    num2 = content.index('</title>', num1)
    title_list.append(content[num1:num2])
    num3 = content.index('<meta name="keywords" content="', beg)+31
    num4 = content.index('<meta name="description" content="', num3)-4
    keyword_list.append(content[num3:num4])
    num5 = content.index('<meta name="description" content="', beg) + 34
    num6 = content.index('<meta name="author"', num5) - 4
    description_list.append(content[num5:num6])
    return title_list,keyword_list,description_list


def classification(content, beg=0):
    strlist = re.findall('[\x80-\xff+]+', content)
    str1 = ' '.join(strlist)
    # print chardet.detect(str1)['encoding']
    # cal = str+' '+str1+' '+str2
    return str1


def connectDatabase(d_b):
    url_list = []
    try:
        conn = MySQLdb.connect(host='', user='', passwd='', db=d_b, port=)
        cur = conn.cursor()

        n = cur.execute('select distinct(f1) from ws_163_tech order by f1 desc')
        res = cur.fetchall()
        for r in res:
            url_list.append(r[0])
            # print len(r[0])
        cur.close()
        conn.close()
        return url_list
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__ == '__main__':
    url_list = connectDatabase('aaa')
    cla_list = []
    text_list = []
    f = open("E:\\163\\Tech\\tech.txt", "a+")
    f1 = open("E:\\163\\Tech\\text.txt", "a+")
    for i in range(0, len(url_list)-1):
        t = url_list[i]
        if len(t)<65 and t[-5:] in ('.html','earch'):
            html = getHtml(t)
            if html != '':
                content_t = content(html, '<head>', '</head>')

                if content_t != '' and "404" not in content_t:
                    content_c = content(html, '<a href="http://www.163.com/"', '正文')
                    if content_c != '' and "网易学院·教程" not in content_c:
                        str1 = classification(content_c, beg=0)
                        cla_list.append(str1)
                        title, keyword, description = title_16(content_t, beg=0)
                        f.write(str(i)+':'+str1+'\n')
                        # f = open("E:\\163\\Car\\Carbuy\\%s.txt"%i, "w+")
                        # f1 = open("163auto_key.txt", "w+")
                        text_list.append(title[0]+','+keyword[0]+','+description[0])
                        f1.write(title[0] + '\n' + keyword[0] + '\n' + description[0] + '\n' + '\n' + '\n')
                    # f.write(title[0]+'\n'+keyword[0]+'\n'+description[0])
                    # f.close()
        # f1.close()
    #   for item in cla_list:
    #       print item.decode('gb2312').encode('utf-8')

    f.close()
    f1.close()