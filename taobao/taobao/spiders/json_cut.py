# coding:utf-8
'''
对获得的网页内容进行url与文字的提取
'''
import simplejson

class JsonCut(object) :

    def json_cut(self):
        # json_str = self.s[49:-13]
        f = open('/crawl/taobao/homepage.txt')
        s = f.readline()
        f.close()

        json_str = s[29:-2]
        jo = simplejson.loads(json_str)

        label_dic = {u'孕产用品':u'孕妇裤 月子服 哺乳文胸 吸奶器 防辐射 孕妇内裤 待产包 孕妇牛仔裤 孕妇营养品 防溢乳垫 美德乐 十月妈咪 三洋 Bravado 新生儿 婴儿床 婴儿推车 抱被 隔尿垫 学步车 安抚奶嘴 纸尿裤',
                     u'奶食':u'爱他美 羊奶粉 特殊配方奶粉 喜宝 惠氏 启赋 牛栏 美素佳儿 贝因美 雅培 美赞臣 可瑞康 a2 嘉宝 美林 溶溶豆 奶片 钙铁锌 DHA 宝宝食用油 宝宝调料 奶瓶 餐具 餐椅 暖奶器',
                     u'生鲜':u'樱桃 海参 麻辣小龙虾 三文鱼 牛排 咸鸭蛋 土鸡蛋 奇异果 土鸡 芒果 橙子 黄秋葵 苹果 榴莲 柠檬 干贝 大闸蟹 虾仁 生蚝 牛肉 虾皮 北极贝 银鳕鱼 车厘子 蔬菜 菠萝蜜 紫薯 山竹 木瓜 牛油果 甜虾 泥螺 土猪肉 青蟹 哈密瓜 花胶'

        }
        fir_lab_lis = [u'孕产用品', u'奶食', u'生鲜']

        sec_dic = {}
        del_lis = []
        for k, v in jo.items():
            fir_lab = v['value']['head'][0]['name']    # 女装
            if fir_lab in fir_lab_lis:
                n = (10000/len(label_dic[fir_lab].split(' ')))/60 + 1
                for i in v['value']['list']:
                    try:
                        if i['name'] in label_dic[fir_lab] and i['link'] not in sec_dic:
                            sec_dic[i['link']] = [fir_lab+' '+i['name'], n]    # 女装 连衣裙：url   每个类取多少条记录
                        elif i['name'] in label_dic[fir_lab] and i['link'] in sec_dic:
                            del_lis.append(i['link'])    # 如果有重复链接，则删除
                    except Exception as e:
                        print e

        for j in del_lis:
            sec_dic.pop(j)

        # f = open('/crawl/taobao/urlstest.txt','w')
        # for i in sec_dic:
        #     f.write(i.encode('utf-8')+'\001'+sec_dic[i][0].encode('utf-8')+'\n')
        # f.close()

        return sec_dic




