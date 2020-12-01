from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import pymongo
import datetime
from django import forms
from django.core.exceptions import ValidationError

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
list = []
database = client.get_database('data')
collections = database.get_collection('hospitals')
source = collections.aggregate([
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
