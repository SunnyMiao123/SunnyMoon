import datetime
import json
import os
import sys
import threading

import pymongo
from bson import json_util
from django import forms
from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.views.decorators.csrf import csrf_exempt
sys.path.append(
    '/Users/sunmiao/Documents/GitHub/SunnyMoon/hospitalproject/backend/adapter/')

import projectsnew as project

if __name__ == "__main__":
    print(sys.path)

class input_form(forms.Form):
    begintime = forms.CharField(
        required=True,
    )
    endtime = forms.CharField(
        required=True,
    )
    keyword = forms.CharField(
        required=True,
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


@csrf_exempt
def deletetask(request):
   # print(request)

    if(request.method == "POST"):
        jsonfile = json.loads(request.body)
        delid = jsonfile['taskid']
        tasks = database.get_collection('tasks')
        datas = database.get_collection('projects_new')
        tasks.delete_one({'taskid': delid})
        datas.delete_many({'taskid':delid})
        return HttpResponse('Success')


def displayalltasks(requst):
    tasks = gettasksdata()

    response = json.dumps(tasks, default=json_util.default)
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
            '$match': {
                'date': datetime.datetime.now().strftime('%Y-%m-%d')
            }},
         {'$group': {
             '_id': '$date',
             'max': {'$max': "$sort"}
         }}
         ]
    )
    li = [t['max'] for t in line]
    ret = 1
    if len(li) > 0:
        ret = li[0]+1
    return ret


@csrf_exempt
def beginPythonData(request):
    je = project.projectsdata()
    print(request.body)
    if(request.method == 'POST'):
        jsonfile = json.loads(request.body)
        try:
            starttime = str.replace(jsonfile['begintime'], '-', ':')
            endtime = str.replace(jsonfile['endtime'], '-', ':')
            keyword = jsonfile['keyword']
            taskid = jsonfile['taskid']
            dat = je.CatchAllAndSave(starttime, endtime, keyword, taskid)
            updatetask(taskid,dat[1],'Closed')
        except:
            updatetask(taskid,0,'Failed')
            return HttpResponse('error')
        else:
            return HttpResponse('Success')


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
                 'end_time', 'file_num', 'keyword', 'date', 'state', 'sort']
        co = [id, starttime,
              endtime, 0, keyword, datetime.datetime.now().strftime('%Y-%m-%d'), 'Open', todaysort]
        one = dict(zip(paras, co))
        tasks.insert_one(one)
        return HttpResponse('Success')
        """
        je = project.projectsdata()
        t = threading.Thread(target= je.CatchAllAndSave,args=('2020:10:01','2020:10:11','医院信息',id))
        t.start()
        """


def updatetask(taskid, filenum, state):
    """
    更新任务列表
    """
    tasks = database.get_collection('tasks')
    
    return tasks.update_one({'taskid': taskid}, {
                     '$set': {"file_num": filenum, "state": state}})
