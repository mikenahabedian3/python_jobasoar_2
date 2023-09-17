from django.contrib import admin
from .models import Company, CompanyUser, JobSeeker, Job

# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyUser)
admin.site.register(JobSeeker)
admin.site.register(Job)
