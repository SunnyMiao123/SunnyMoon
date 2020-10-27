import csv
import io
import json
import re
import uuid

import requests
import urllib3
from bs4 import BeautifulSoup
from lxml import etree


class pyData:
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
    paralist = ['id', 'name', 'cost', 'region', 'url', 'date',
                'depart', 'agent', 'type', 'province']
    pylist = []
    pyjson = ''
    baseUrl = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1'
    keyword = '医院信息'
    start_time = '2020-01-01'
    end_time = '2020-10-26'
    page_num = 1
    params = {
        'searchtype': '2',
        'page_index': page_num,
        'bidSort': '0',
        'pinMu': '0',
        'bidType': '0',
        'kw': keyword,
        'start_time': start_time,
        'end_time': end_time,
        'timeType': '6'
    }
    headers = {
        'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
        'Host': 'search.ccgp.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36'
    }

    def beginread(self):
        response = requests.get(
            self.baseUrl, headers=self.headers, params=self.params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
        else:
            soup = BeautifulSoup(response.content, 'lxml')
        ss = soup.find('span')
        li = soup.find('ul', attrs={'class': 'vT-srch-result-list-bid'})
        if li != None:
            alllist = []
            for i in li.find_all('li'):
                li2 = [str(uuid.uuid1())]
                li2.append(i.find('a').get_text().strip())
                web = i.find('a')['href']
                #  detail=requests.get(web).content
                sp = BeautifulSoup(requests.get(web).content, 'lxml')
                ys = ''
                region = ''
                for tt in sp.find('table').find_all('td', string=re.compile('金额')):
                    ys = tt.parent.find_all('td')[1].get_text()
                li2.append(ys)
                for tt in sp.find('table').find_all('td', string=re.compile('行政区域')):
                    region = tt.parent.find_all('td')[1].get_text()
                li2.append(region)
                li2.append(i.find('a')['href'])
                li2.append(i.find('span').get_text().split('|')[0].strip())
                li2.append(i.find('span').get_text().split('|')[1].strip())
                li2.append(i.find('span').get_text().split(
                    '|')[2].split('\n')[0].strip())
                li2.append(i.find('span').find('strong').get_text().strip())
                li2.append(i.find('span').find('a').get_text().strip())
              #  li2.append(
              #      sp.find(attrs={'class': 'vF_detail_content'}).get_text())
                alllist.append(dict(zip(pyData.paralist, li2)))

            self.pylist.extend(alllist)
        else:
            print('No Data found!')
    def run(self):
        for i in range(1,7):
            print('正在爬取第{}页'.format(str(i)))
            self.params['page_index']=i
            self.beginread()

def main():
    pyd=pyData()
    pyd.run()


if __name__ == '__main__':
    main()
