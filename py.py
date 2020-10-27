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
                'depart', 'agent', 'type', 'province', 'content']
    pylist = []
    pyjson = ''
    def beginread(pageIndex):
        
        website = "http://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index={0}&bidSort=&buyerName=&projectId=&pinMu=&bidType=1&dbselect=bidx&kw=%E5%8C%BB%E9%99%A2%E4%BF%A1%E6%81%AF&start_time=2019%3A02%3A01&end_time=2019%3A08%3A02&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName=".format(pageIndex)
      #  print(website)
        sourcehtml = requests.get(website).content
        soup = BeautifulSoup(sourcehtml, 'lxml')
        ss=soup.find('span')
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
                li2.append(
                    sp.find(attrs={'class': 'vF_detail_content'}).get_text())
                alllist.append(dict(zip(pyData.paralist, li2)))
          #  print(alllist)
            pyData.pylist.extend(alllist)
         #   print(len(alllist))
        else:
            print('No Data found!')
    def getList():
        for tar in range(1,25):
            pyData.beginread(tar)
        print(len(pyData.pylist))
def main():
    for tar in range(1,25):
        pyData.beginread(tar)
    print(len(pyData.pylist))



if __name__ == '__main__':
    main()
