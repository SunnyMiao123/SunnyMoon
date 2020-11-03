import pymongo
import requests
from bs4 import BeautifulSoup
import re
import lxml
import os

client = pymongo.MongoClient(host='127.0.0.1',port=27017)

db=client['data']
collection=db['projects']
filestream=db['files']

list=collection.find({"type":"公开招标公告","id":"66aa2618-18c4-11eb-bcd7-acde48001122"})

for target_list in list:
    response = requests.get(target_list["url"])
    if response.status_code==200:
        html=response.content
        soup=BeautifulSoup(html,'lxml')
        target = soup.find_all(attrs={'class':'bizDownload'})
        for item in target:
            doc=requests.get('http://www.ccgp.gov.cn/oss/download?uuid={}'.format(item['id'])).content
            path=os.path.curdir+'/1.doc'
            print(path)
            with open(path,'wb') as target:
                target.write(doc)
    else:
        pass

