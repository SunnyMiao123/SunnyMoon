from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import pymongo
import datetime
from django import forms
from django.core.exceptions import ValidationError

class input_form(forms.Form):
    starttime = forms.DateField()
    endtime = forms.DateField()
    keyword = forms.CharField()

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
list = []
database = client.get_database('data')

def gettasksdata():
    tasks = database.get_collection('tasks')
    tasksdata = []
    for t in tasks.find():
        tasksdata.append(t)
    return tasksdata


def deletetask(request):
    if(request.method == "POST"):
        delid = request.POST['id']
        tasks = database.get_collection('tasks')
        tasks.delete_one({'taskid':delid})
    return render(request, 'data.html', {'tasksdata': gettasksdata()})


def dataspy(request):
    if(request.method == "POST"):
        logform = input_form()
        starttime = request.POST['starttime']
        endtime = request.POST['endtime']
        keyword = request.POST['keyword']
        tasks = database.get_collection('tasks')
        paras = ['taskid', 'begin_time',
                 'end_time', 'file_num', 'date', 'state']
        co = [datetime.datetime.now().strftime('%Y%m%d')+'-001', starttime,
              endtime, 0, datetime.datetime.now().strftime('%Y-%m-%d'), 'Open']
        one = dict(zip(paras, co))
        tasks.insert_one(one)
        return render(request, 'data.html', {'tasksdata': gettasksdata()})
    else:

        return render(request, 'data.html', {'tasksdata': gettasksdata()})