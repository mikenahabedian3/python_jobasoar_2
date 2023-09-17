# jobasoar3/jobasoar3/urls.py

from django.contrib import admin
from django.urls import path, include
from core import views


urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),

]