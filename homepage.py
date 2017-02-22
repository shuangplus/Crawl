# coding:utf-8
'''

# ---------------------------------------
# 网易新闻小爬虫
# ---------------------------------------
# 简介 : 通过分析 www.163.com ，分析其中以 news.163.com 开头的链接
#        获取 各链接的内容，并合并到 163News.txt 以便查看各新闻。
# ---------------------------------------

@author = not me

'''
import re, urllib

strTitle = ""
strTxtTmp = ""
strTxtOK = ""
# list1 = ['cxshhz','jsdjthz','jtpchz','rcpkhz','sjslhz','wqdghz','wysjhz','xcdbhz']
list1 = []
for item in list1:
    f = open("E:\\Corpus\\163\\Car\\163auto%s.txt"%item, "w+")
    for i in range(2,9):
        m = re.findall(r"auto\.163\.com/\d.+?<\/a>",urllib.urlopen("http://auto.163.com/special/%s_0%s/"%(item,i)).read(),re.M)  #
        for i in m:
            testUrl = i.split('"')[0]
            if testUrl[-4:-1]=="htm":

            # 合并标题头内容
                strTitle = strTitle + "\n" + i.split('"')[0]
            # 重新组合链接
                okUrl = i.split('"')[0]
                UrlNews = ''
                UrlNews = "http://" + okUrl

                # print UrlNews

                # 查找分析链接中正文内容。
                # 整理去掉部分 html 代码，让文本更易于观看。
                n = re.findall(r"<P style=.TEXT-INDENT: 2em.>(.*?)<\/P>",urllib.urlopen(UrlNews).read(),re.M)
                for j in n:
                    if len(j)<>0:
                        j = j.replace("&nbsp", "\n")
                        j = j.replace("<STRONG>", "\n_____")
                        j = j.replace("</STRONG>", "_____\n")
                        strTxtTmp = strTxtTmp + j + "\n"
                        strTxtTmp = re.sub(r"<a href=(.*?)>", r"", strTxtTmp)
                        strTxtTmp = re.sub(r"<\/[Aa]>", r"", strTxtTmp)

            # 组合链接标题和正文内容
                strTxtOK = strTxtOK + "\n\n\n===============" + i.split('"')[0] + i.split('"')[1] + "===============\n" + strTxtTmp
                strTxtTmp = ""
                # print strTxtOK

# 全部分析完成后，写入文件，关闭
    f.write(strTitle)
    f.close()

