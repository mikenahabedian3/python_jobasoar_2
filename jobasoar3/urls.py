# jobasoar3/jobasoar3/urls.py

from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),  # Add this line for the signup view
    path('dashboard/', views.dashboard, name='dashboard'),  # Updated to use views.dashboard
]
