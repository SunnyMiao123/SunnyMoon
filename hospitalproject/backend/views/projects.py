import pymongo
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from bson import json_util
import datetime
import json
import decimal
import bson.decimal128 as decimal128
import requests
from bs4 import BeautifulSoup
import lxml
import os
import urllib.request

"""
获取所有项目数据
"""
def getAllProjects(request):
    client = pymongo.MongoClient('127.0.0.1', 27017)
    projects = client.get_database('data').get_collection('projects_new')
    page = int(request.GET['page'])-1
    percount = int(request.GET['percount'])

    lists = []
    for t in projects.find({}).skip(page*percount).limit(percount):
        lists.append({'taskid': t['taskid'], 'date': datetime.datetime.strftime(t['date'], '%Y-%m-%d'), 'province': t['province'],
                      'name': t['name'], 'cost': str(decimal128.Decimal128(str(t['cost'])).to_decimal().quantize(decimal.Decimal('0.00'))), 
                      'type': t['type'], 'region': t['region'], 'url': t['url'], 'projectid': t['projectid'], 'depart': t['depart'], 'agent': t['agent']})
    fill = json.dumps(lists, default=json_util.default)
    return HttpResponse(fill)

def getListByCondition(request):
    """
    docstring
    """
    client = pymongo.MongoClient('127.0.0.1', 27017)
    projects = client.get_database('data').get_collection('projects_new')
    condition = request.GET['taskid']
    print(condition)
    retList= []

    for t in projects.find({"$or":[{"taskid":condition},{"html":{'$regex':condition}}]}):
        retList.append({'taskid': t['taskid'], 'date': datetime.datetime.strftime(t['date'], '%Y-%m-%d'), 'province': t['province'],
                      'name': t['name'], 'cost': str(decimal128.Decimal128(str(t['cost'])).to_decimal().quantize(decimal.Decimal('0.00'))), 
                      'type': t['type'], 'region': t['region'], 'url': t['url'], 'projectid': t['projectid'], 'depart': t['depart'], 'agent': t['agent']})
    jsonStr= json.dumps(retList,default=json_util.default)

    return HttpResponse(jsonStr)


"""
下载文件
"""
def downloadfiles(request):
    """
    下载文件
    """
    taskid = request.GET['taskid']
    client = pymongo.MongoClient('127.0.0.1', 27017)
    projects = client.get_database('data').get_collection('projects_new')
    headers = {
        'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
        'Host': 'www.ccgp.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36'
    }


    for item in projects.find({'taskid':taskid}):
        if str(item['html']).find('附件',0,-1)>0:
           # print(item['projectid'],item['name'])
            soup = BeautifulSoup(requests.get(item['url']).content,'lxml')
            target = soup.findAll(attrs={'class':'bizDownload'})
            for i in target:
                response=requests.get(url='http://www.ccgp.gov.cn/oss/download?uuid={}'.format(i['id']),headers=headers)
                #if response.status_code==200:
                print(response.status_code)
                doc = response.content
                print ('http://www.ccgp.gov.cn/oss/download?uuid={}'.format(i['id']))

                path=os.path.curdir+'/docments/'+item['name']
                if os.path.exists(path)==False:
                    os.makedirs(path)
                dirs = path+'/'+i.text
                with open(dirs,'wb') as t:
                    t.write(doc)
            
    tasks = client.get_database('data').get_collection('tasks')
    tasks.update_one({'taskid': taskid}, {
                     '$set': { "state": 'Finish'}})
    return HttpResponse('Success')

def getProjectsNums(requests):
    """
    docstring
    """
    
    return HttpResponse('Success')