# jobasoar3/jobasoar3/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    # path('signup/', views.signup, name='signup'),  # Add this line for the signup view
    path('dashboard/', views.dashboard, name='dashboard'),  # Updated to use views.dashboard
    path('upload_xml/', views.upload_xml, name='upload_xml'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<str:reference_id>/', views.job_detail, name='job_detail'),  # Only reference_id pattern
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
