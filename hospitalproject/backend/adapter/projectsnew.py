import decimal
import re
import requests

import csv
import os
from bs4 import BeautifulSoup
import lxml
import pymongo
import sys
import uuid
import math
import bson.decimal128 as decimal128
import datetime
import time
sys.path.append('..')
import dbmanager as manager

class projectsdata:

    def __init__(self):
        super().__init__()

    host = '127.0.0.1'
    port = 27017

    headers = {
        'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
        'Host': 'search.ccgp.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36'
    }

    baseURL = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1'

    def save(self, projectlist):
        """
        docstring
        """
        client = manager.dbmanager().ConnectDB()
        data = client.get_database('data')
        projects = data.get_collection('projects_new')
        return projects.insert(projectlist)

    def delete(self, id):
        """
        docstring
        """
        client = manager.dbmanager().ConnectDB()
        data = client.get_database('data')
        projects = data.get_collection('projects_new')
        return projects.delete_one({'id': id})

    def listallprojects(self, filter):
        """
        docstring
        """
        client = manager.dbmanager().ConnectDB()
        data = client.get_database('data')
        projects = data.get_collection('projects')
        if filter == None:
            return [t for t in projects.find()]
        else:
            return [t for t in projects.find(filter)]

    def pageBaseData(self, begintime, endtime, keyword, pageindex):
        """
        从网页抓取数据
        """
        params = {
            'searchtype': '2',
            'page_index': pageindex,
            'bidSort': '0',
            'pinMu': '0',
            'bidType': '0',
            'kw': keyword,
            'start_time': begintime,
            'end_time': endtime,
            'timeType': '6'}
        
        response = requests.get(
            url=self.baseURL, headers=self.headers, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            a = soup.find('span', text=keyword).parent
            tot = int(a.findAll('span')[1].text)
            page = math.ceil(tot/20)
            return soup, tot, page

        else:
            raise BaseException()

    def CatchAll(self, begintime, endtime, keyword,taskid):
        """
        获取全部数据
        """
        print('------Begin Python Service！-------')
        result =  self.pageBaseData(
            begintime=begintime, endtime=endtime, keyword=keyword, pageindex=1)
        maxpage = int(result[2])
        docnum = int(result[1])
        print('本次关键字为【{}】,在【{}】-【{}】时间范围内共获取到 {} 个数据，分{}页'.format(keyword,begintime,endtime,docnum,maxpage))
        retlist = []
        for i in range(1, maxpage+1):
            print('----开始爬取第[{}]页-----'.format(str(i)))
            
            if i == 1:
                temp = result[0]
            else:
                temp = self.pageBaseData(
                begintime=begintime, endtime=endtime, keyword=keyword, pageindex=i)[0]
            li = temp.find('ul', attrs={'class': 'vT-srch-result-list-bid'})
            if li != None:
                for child in li.find_all('li'):
                    time1 = datetime.datetime.now()
                    tid = uuid.uuid1()
                    name = child.find('a').get_text().strip()
                    url = child.find('a')['href']
                    cost = decimal128.Decimal128('0')
                    
                    region = ''
                    ys = ''
                    sp = BeautifulSoup(requests.get(url).content, 'lxml')
                    if sp.find('table') != None:
                        for tt in sp.find('table').find_all('td', string=re.compile('金额')):
                            ys = tt.parent.find_all('td')[1].get_text()
                            yscost = re.findall("\d*[.]\d*", ys)
                            if len(yscost) > 0:
                                cost = decimal128.Decimal128(yscost[0])
                        for tt in sp.find('table').find_all('td', string=re.compile('行政区域')):
                            region = tt.parent.find_all('td')[1].get_text()
                    html = sp.text
                    date = child.find('span').get_text().split('|')[0].strip()
                    if re.match(re.compile(r"^[0-9]{4}.[0-9]{2}.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}"),date)!=None:
                        date = datetime.datetime.strptime(date,'%Y.%m.%d %H:%M:%S')
                    else:
                        date = datetime.datetime.strptime('1900-01-01','%Y-%m-%d')
                    depart = str(child.find('span').get_text().split('|')[
                        1].strip()).replace('采购人：','')
                    agent = str(child.find('span').get_text().split(
                        '|')[2].split('\n')[0].strip()).replace('代理机构：','')
                    typ = child.find('span').find('strong').get_text().strip()
                    province = child.find('span').find('a').get_text().strip()
                    instance = {'projectid': tid, 'name': name,
                                'cost': cost, 'region': region, 'url': url, 
                                'date': date, 'depart': depart, 'agent':agent,
                                'type': typ, 'province': province,'taskid':taskid,'html':html}
                    retlist.append(instance)
                    time2 = datetime.datetime.now()
                    print(name,'耗时：',str(time2 - time1))
            else:
                return None
        return retlist,docnum
    def CatchAllAndSave(self,begintime,endtime,keyword,taskid):
        """
        docstring
        """
        lis = self.CatchAll(begintime= begintime,endtime=endtime,keyword= keyword,taskid= taskid)
        save = self.save(lis[0])
        print('----爬取完成----')
        return save,lis[1]


if __name__ == "__main__":
    """
    data=projectsdata()
    lis = data.CatchAll('2020:12:24','2020:12:31','医院信息','2')
    """
    """
    str = '￥80.400000 万元（人民币）'
    print(decimal.Decimal(re.findall(r"\d*[.]\d*", str)[0]))
    """
    """
    data = projectsdata()
    lis = data.CatchAllAndSave('2020:10:01', '2020:10:11', '医院信息','2')
    print(data.save(lis))
    """

  #  data = '2020.11.11 16:28:15'

 #   print(re.match(re.compile(r"^[0-9]{4}.[0-9]{2}.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}"),data))

  #  print(datetime.datetime.strptime(data,'%Y.%m.%d %H:%M:%S'))
    """
    client = manager.dbmanager().ConnectDB()
    t = client.get_database('data')
    c = t.get_collection('tt')
    data = {'date':datetime.datetime.strptime(data,'%Y.%m.%d %H:%M:%S')}
    c.insert(data)
    """
#print(datetime.datetime.now())