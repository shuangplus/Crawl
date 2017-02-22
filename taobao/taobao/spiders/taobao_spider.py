# coding:utf-8
"""
一个简单的Python 爬虫, 用于抓取淘宝网的商品类别等
Anthor: WS
Version: 0.0.1
Date: 2017-1-9
Language: Python2.7
Editor: Pycharm
Operate:
"""

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from taobao.items import TaobaoItem
from json_cut import JsonCut
import scrapy, copy,chardet
from scrapy import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class TaobaoSpider(scrapy.Spider) :
    name = "taobao"
    allowed_domains = ["www.taobao.com"]

    # start_urls = [
    #     "https://tce.alicdn.com/api/data.htm?ids=222887%2C222890%2C222889%2C222886%2C222906%2C222898%2C222907%2C222885%2C222895%2C222878%2C222908%2C222879%2C222893%2C222896%2C222918%2C222917%2C222888%2C222902%2C222880%2C222913%2C222910%2C222882%2C222883%2C222921%2C222899%2C222905%2C222881%2C222911%2C222894%2C222920%2C222914%2C222877%2C222919%2C222915%2C222922%2C222884%2C222912%2C222892%2C222900%2C222923%2C222909%2C222897%2C222891%2C222903%2C222901%2C222904%2C222916%2C222924&callback=jsonp1021"]
    # print '*************************url****************************'
    # rules = (
    #     #将所有符合正则表达式的url加入到抓取列表中
    #     Rule(SgmlLinkExtractor(allow = (r'http://movie\.douban\.com/top250\?start=\d+&filter=&type=',))),
    #     #将所有符合正则表达式的url请求后下载网页代码, 形成response后调用自定义回调函数
    #     Rule(SgmlLinkExtractor(allow = (r'http://movie\.douban\.com/subject/\d+', )), callback = 'parse_page', follow = True),
    #     )


    def start_requests(self):
        print '*************************url****************************'
        urls = {}

        jc = JsonCut()
        sec_info = jc.json_cut()

        print 'sites*****************************'
        print len(sec_info)

        for i in sec_info:
            if 'https:' not in i[:10]:
                ur = 'https:' + i
            else:
                ur = i
            urls[ur] = sec_info[i]
            for l in range(1, sec_info[i][1]):
                urls[ur + '&bcoffset=12&s=' + str(l * 60)] = sec_info[i][0]

        print 'urls_len*****************************'
        print len(urls)
        print '*****************************'

        for url in urls:
            yield Request(url=url,meta={'label':urls[url]})



    def parse(self, response):


        # print "============================="
        # print response
        # content = response.xpath('//body').extract()  # div[@class="service-float-item clearfix"]
        # # print content[0].encode('gbk')
        # jc = JsonCut(content[0])
        # sec_info = jc.json_cut()
        #


        # f = open('F:/WS/guanyi/coding/PycharmProjects/crawl/taobao/urls1.txt','w')
        # for url in urls:
        #     f.write(url.encode('gbk')+','+urls[url][0].encode('gbk')+','+str(urls[url][1])+'\n')
        #     # yield Request(url, callback=self.parse)
        # f.close()


        print 'parse*****************************'
        print response.url
        item = TaobaoItem()

        item['script'] = response.xpath('//script').extract()
        # print item['script']
        output = open('/crawl/taobao/samples6.txt', 'a')
        for sel in item['script']:
            if 'g_page_config' in sel:
                ui = sel.split(',')
                for i in ui:
                    if 'raw_title' in i:
                        if type(i.split(':')[1]) == 'list':
                            print i.split(':')[1]
                        else:
                            output.write(response.meta['label'].encode('utf-8') + '\001' +
                                         i.split(':')[1][1:-1].encode('utf-8') + '\n')
        output.close()
        # if item['script'] != []:
        #     yield item










    # def parse(self, response):
    #     item = TaobaoItem()
    #     # sites = hxs.select('//div[@class="home-category-list J_Module"]')
    #     sites = response.xpath('//div[@class="home-category-list J_Module"]')
    #
    #     item['firstlabel'] = []
    #     item['secondlabel'] = []
    #     item['keyword'] = []
    #     t = 0
    #     for sel in sites:
    #
    #         firstlabel = sel.xpath('div/a[@class="category-name category-name-level1 J_category_hash"]/text()') \
    #             .extract()[0].encode('utf-8')
    #
    #         for sec in sel.xpath('div/ul/li'):
    #             t += 1
    #             print t
    #             secondlabel = sec.xpath('a/text()').extract()[0].encode('utf-8')
    #             keyword_lis = sec.xpath('div/a/text()').extract()
    #
    #             item['firstlabel'] = firstlabel  # 大类  '女装男装'
    #             item['secondlabel'] = secondlabel  # '潮流女装'
    #             item['keyword'] = ' '.join([i.encode('utf-8') for i in keyword_lis])  # '羽绒服','连衣裙'
    #
    #             yield item
                # print '************************title*****************************'
                # print firstlabel, secondlabel
                # print '************************title*****************************'

                # sel = Selector(response)
                # item = TaobaoItem()
                # item['label'] = sel.xpath('//div/a[@class="category-name category-name-level1 J_category_hash"]/text()')\
                #                   .extract()[0].encode('utf-8')

                # '//body/a[@class="category-name category-name-level1 J_category_hash"]/text()'
                # item['description'] = sel.xpath('//div/span[@property="v:summary"]/text()').extract()
                # item['url'] = response.url
                # print item['label']


