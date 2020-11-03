from django.http import HttpResponse
from django.shortcuts import render,render_to_response
import pymongo

client=pymongo.MongoClient(host='127.0.0.1',port=27017)
data=client['data']
collecions=data[
'hospitals'
]

hospitals=collecions.find({},{'name':1,'province':1,'city':1,'level':1,'_id':0,'location':1})
list=[]
for target in hospitals:
    list.append(target)
def hello(request):
    return render(request,'index.html',{'data':list})

def dataspy(request):
    return render(request,'data.html')