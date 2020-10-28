import requests
from bs4 import BeautifulSoup
import re
import json
import pymongo

class Hospital:
    def __init__(self):
        self.website=""
        pass
    website="http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8"
    rootweb="http://www.a-hospital.com/w/"
    districts=[]
    hoslist=[]
    columns=['name','location','level','province','method','website']
    def getHospitalList(self):
        html=requests.get(Hospital.website).content
        soup=BeautifulSoup(html,'lxml')
        topic=soup.find(id='toc').findAll('ul')[0].findAll('li',class_='toclevel-2')
        for li in topic:        
            Hospital.districts.append(li.find('span',class_='toctext').string)
     #   print(Hospital.districts)
        for province in Hospital.districts:
            newweb=Hospital.rootweb+province+'医院列表'
            deta=requests.get(newweb).content
            desoup=BeautifulSoup(deta,'lxml')
            hos=desoup.find('ul').findAll('ul')
            datalist=[]
            for h in hos:
                applist=[]
                t0=h.find_parent('li').find('a').string
                applist.append(t0)
                t1=h.find(string=re.compile('地址'))
               # print(t1.next_element[1:] if t1 is not None else '') 
                applist.append(t1.next_element[1:] if t1 is not None else '')
                t2=h.find(string=re.compile('等级'))
                #print(t2.next_element[1:] if t2 is not None else '')
                applist.append(t2.next_element[1:] if t2 is not None else '')
                #print(province)
                applist.append(province)
                t3=h.find(string=re.compile('经营'))
                #print(t3.next_element[1:] if t3 is not None else '')
                applist.append(t3.next_element[1:] if t3 is not None else '')
                t4=h.find(string=re.compile('网站'))
               # print(t4.next_element[1:] if t4 is not None else '')
                applist.append(t4.next_element[1:] if t4 is not None else '')
             #   print(h.findAll('li')[1].string)
               # print(h.findAll('li')[2].string)
               # print('---------------------')
                temp=dict(zip(Hospital.columns,applist))
                jsonstr=json.dumps(temp)
                client=pymongo.MongoClient(host='localhost',port=27017)
                db=client['data'
                ]
                colletion=db['hospitals']
                colletion.insert_one(temp)
               # datalist.append(temp)
          #  Hospital.hoslist.append(datalist)
       # print(Hospital.hoslist)
if __name__ == "__main__":
    Hospital.getHospitalList()
  