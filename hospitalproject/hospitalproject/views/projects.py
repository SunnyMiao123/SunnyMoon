import pymongo
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from bson import json_util
import datetime
import json
import decimal
import bson.decimal128 as decimal128


def getAllProjects(request):
    """
    获取所有项目数据
    """
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