import requests
from bs4 import BeautifulSoup
import re
import json
import pymongo


class Hospital:
    def __init__(self):
        self.website = ""
        pass
    website = "http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8"
    rootweb = "http://www.a-hospital.com/"
    districts = []
    hoslist = []
    columns = ['name', 'location', 'level', 'province', 'method', 'website']

    def getHospitalList(self):
        html = requests.get(Hospital.website).content
        soup = BeautifulSoup(html, 'lxml')
        topic = soup.find(id='toc').findAll(
            'ul')[0].findAll('li', class_='toclevel-2')
        for li in topic:
            Hospital.districts.append(li.find('span', class_='toctext').string)
     #   print(Hospital.districts)
        for province in Hospital.districts:
            newweb = Hospital.rootweb+province+'医院列表'
            deta = requests.get(newweb).content
            desoup = BeautifulSoup(deta, 'lxml')
            # print(desoup.findAll('p')[1])
            for city in desoup.findAll('p')[1].findAll('a', href=True):
                print(city['href'], city['title'], city.string)
                tmpweb = rootweb+city['href']
                try:
                    response = requests.get(tmpweb)

                    html = response.content
                    desoup = BeautifulSoup(html, 'lxml')
                    hos = desoup.find('ul').findAll('ul')
                    print(hos)
                    datalist = []
                    for h in hos:
                        applist = []
                        t0 = h.find_parent('li').find('a').string
                        print(t0)

                except:
                    return


if __name__ == "__main__":
    hos = Hospital()
    hos.getHospitalList()
