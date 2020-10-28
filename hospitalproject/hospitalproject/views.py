from django.http import HttpResponse
from django.shortcuts import render,render_to_response

def hello(request):
    return render(request,'index.html')