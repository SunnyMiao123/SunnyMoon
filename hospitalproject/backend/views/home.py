from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import pymongo
import datetime
from django import forms
from django.core.exceptions import ValidationError
import json

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
list = []
database = client.get_database('data')
hoscollections = database.get_collection('hospitals')
procollections = database.get_collection('projects_new')
taskscollection = database.get_collection('tasks')
source = hoscollections.aggregate([
    {
        '$group': {
            '_id': '$province',
            'value': {'$sum': 1}

        }
    }
])
for target in source:
    list.append(target)
cols = [t['_id'] for t in list]
vals = [t['value']for t in list]


def hello(request):
    return render(request, 'index.html', {'data': list, 'cols': cols, 'vals': vals})


def datashow(request):
    return render(request, 'datashow.html')


def getbasenum(request):
    """
    docstring
    """
    fileTotnum = procollections.count()

    hospitalTotNum = hoscollections.count()
    tasksnum = taskscollection.count()
    prov= procollections.aggregate([
    {
        '$group': {
            '_id': '$province', 
            '数量': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            '数量': -1
        }
    }
])
    jsonfile = json.dumps({
        'fileTotNum': fileTotnum,
        'hosTotNum': hospitalTotNum,
        'tasksTotNum': taskscollection.count(),
        'fileStatics':{
            'colunms':['_id','数量'],
            'rows':[i for i in prov]
        }
    })
    return HttpResponse(jsonfile)


def getStaticsNum(request):
    prov= procollections.aggregate([
        {
            '$group': {
                '_id': '$province',
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    for item in prov:
        print(item)


if __name__ == "__main__":
    getStaticsNum('')
