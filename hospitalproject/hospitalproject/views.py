from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import pymongo
import datetime

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
list = []
database = client.get_database('data')
collections = database.get_collection('hospitals')
hospitals = collections.find(
    {}, {'name': 1, 'province': 1, 'city': 1, 'level': 1, '_id': 0, 'location': 1})
source=collections.aggregate([
    {
        '$group':{
            '_id':'$province',
            'value':{'$sum':1}

        }
    }
])
for target in source:
    list.append(target)
cols=[t['_id'] for t in list]
vals=[t['value']for t in list]

projects = database.get_collection('projects')
p = projects.find_one()
print(type(datetime.datetime.strptime(p['date'],'%Y.%m.%d %H:%M:%S')))

#i = projects.update_many({},{'$set':{'depart':str.replace('depart','采购人：','')}})

#print(projects.find_one())
#{'_id': ObjectId('5f98c6ae78109ab4cd9a4ef4'),
#  'id': '59465fa4-18bb-11eb-83fe-acde48001122', 
# 'name': '厦门大学附属中山医院厦门万翔-竞争性磋商-XM2020-TZ0500-网络安全等保测评成交结果公告成交公告', 
# 'cost': '￥24.480000 万元（人民币）',
#  'region': '福建省',
#  'url': 'http://www.ccgp.gov.cn/cggg/dfgg/cjgg/202010/t20201027_15312047.htm', 
# 'date': '2020.10.27 14:15:53', 'depart': '采购人：厦门大学附属中山医院', 
# 'agent': '代理机构：厦门万翔招标有限公司', 
# 'type': '成交公告', 
# 'province': '福建'}


def hello(request):
    return render(request, 'index.html', {'data': list,'cols':cols,'vals':vals})


def dataspy(request):
    return render(request, 'data.html')


def datashow(request):
    return render(request, 'datashow.html')
