import json
import re

import pymongo
import requests
from bs4 import BeautifulSoup


class Hospital:
    def __init__(self):
        self.website = ""
        pass
    website = "http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8"
    rootweb = "http://www.a-hospital.com/"
    districts = []
    hoslist = []
    columns = ['name', 'location', 'level',
               'province', 'city', 'method', 'website']

    def getHospitalList(self):
        html = requests.get(Hospital.website).content
        soup = BeautifulSoup(html, 'lxml')
        topic = soup.find(id='toc').findAll(
            'ul')[0].findAll('li', class_='toclevel-2')
        for li in topic:
            Hospital.districts.append(li.find('span', class_='toctext').string)
     #   print(Hospital.districts)
        for province in Hospital.districts:
            newweb = Hospital.rootweb+'w/'+province+'医院列表'
            deta = requests.get(newweb).content
            desoup = BeautifulSoup(deta, 'lxml')
            # print(desoup.findAll('p')[1])
            for city in desoup.findAll('p')[1].findAll('a', href=True):
                print(city['href'], city['title'], city.string)
                tmpweb = Hospital.rootweb+city['href']
                try:
                    response = requests.get(tmpweb)

                    html = response.content
                    desoup = BeautifulSoup(html, 'lxml')
                    hos = desoup.findAll('ul')[2].findAll('ul')
                    if len(hos)==0:
                        hos=desoup.findAll('ul')[3].findAll('ul')
                    print(len(hos))
                    datalist = []
                    for h in hos:
                        applist = []
                        try:
                            applist.append(h.find_parent('li').find('a').string)
                            t1 = h.find(string=re.compile('地址'))
                            applist.append(
                                t1.next_element[1:] if t1 is not None else '')
                            t2 = h.find(string=re.compile('等级'))
                            applist.append(
                                t2.next_element[1:] if t2 is not None else '')
                            applist.append(province)
                            applist.append(city.string)
                            t3 = h.find(string=re.compile('经营'))
                            applist.append(
                                t3.next_element[1:] if t3 is not None else '')
                            t4 = h.find(string=re.compile('网站'))
                            applist.append(
                                t4.next_element[1:] if t4 is not None else '')
                            temp=dict(zip(Hospital.columns,applist))
                            jsonstr=json.dumps(temp)
                            client=pymongo.MongoClient(host='127.0.0.1',port=27017)
                            db=client['data']
                            collecion=db['hospitals']
                            collecion.insert_one(temp)
                        except:
                            continue
                except:
                    return


if __name__ == "__main__":
    hos = Hospital()
    hos.getHospitalList()
