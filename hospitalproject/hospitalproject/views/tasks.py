from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import pymongo
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
import threading
from django.core import serializers 
import json
import sys
from bson import json_util
sys.path.append('/Users/sunmiao/Documents/GitHub/SunnyMoon/hospitalproject/hospitalproject/adapter')
import os
import projectsnew as project
from django.views.decorators.csrf import csrf_exempt

class input_form(forms.Form):
    begintime = forms.CharField(
        required= True,
    )
    endtime = forms.CharField(
        required= True,
    )
    keyword = forms.CharField(
        required = True,
    )

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
    print(request)
    if(request.method == "POST"):
        delid = request.POST['taskid']
        tasks = database.get_collection('tasks')
        tasks.delete_one({'taskid':delid})
    return redirect('/pydata/')

def displayalltasks(requst):
    tasks= gettasksdata()

    response=json.dumps(tasks,default=json_util.default)
    return HttpResponse(response)

def showalltasks(request):
    """
    显示所有已经执行的计划任务
    """
    return render(request, 'task-display.html', {'tasksdata': gettasksdata()})

def gettodayMaxsort(collection):
    """
    获取当日最大流水号
    """
    line = collection.aggregate(
        [{
               '$match':{
                   'date':datetime.datetime.now().strftime('%Y-%m-%d')
               }},
               {'$group' :{
                   '_id':'$date',
                   'max':{'$max':"$sort"}
               }}
           ]
    )
    li = [t['max'] for t in line]
    ret = 1
    if len(li) > 0:         
        ret = li[0]+1
    return ret

@csrf_exempt
def addtask(request):
    """
    POST请求，增加一个计划任务
    """
    if (request.method == 'POST'):
        jsonfile = json.loads(request.body)

        starttime = jsonfile['begintime']
        endtime = jsonfile['endtime']
        keyword = jsonfile['keyword']
        tasks = database.get_collection('tasks')
            
        todaysort = gettodayMaxsort(tasks)
        id = datetime.datetime.now().strftime('%Y%m%d')+"-"+str(todaysort).zfill(3)
        paras = ['taskid', 'begin_time',
                 'end_time', 'file_num','keyword', 'date', 'state','sort']
        co = [id, starttime,
              endtime, 0, keyword ,datetime.datetime.now().strftime('%Y-%m-%d'), 'Open',todaysort]
        one = dict(zip(paras, co))
        tasks.insert_one(one)
        return HttpResponse('Success')     
        """
        je = project.projectsdata()
        t = threading.Thread(target= je.CatchAllAndSave,args=('2020:10:01','2020:10:11','医院信息',id))
        t.start()
        """
        
                
    

