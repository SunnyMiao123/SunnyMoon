"""hospitalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import hospitalproject.views.home as view
import hospitalproject.views.tasks as tasks
import hospitalproject.views.projects as projects

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',view.hello),
    path('pydata/',tasks.showalltasks),
    path('datashow/',view.datashow),
    path('pydata/deletetask/', tasks.deletetask),
    path('pydata/addtask/',tasks.addtask),
    path('pydata/displayalltasks/',tasks.displayalltasks),
    path('pydata/beginPythonData/',tasks.beginPythonData),
    path('pydata/projects/getall/',projects.getAllProjects),
    path('pydata/downloadfile/',projects.downloadfiles),
    path('pydata/home/getBaseNum/',view.getbasenum),
]