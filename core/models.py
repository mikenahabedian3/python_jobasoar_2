from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string

# the model should have fields to store the narrative text, job seeker's ID (to link the narrative to a specific user), and dates
class JobSeekerNarrative(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    narrative_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    xml_file = models.FileField(upload_to='xmls/', null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


def create_reference_id():
    return get_random_string(length=16)


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('hourly', 'Hourly'),
    ]

    xml_job_id = models.CharField(max_length=255, null=True, blank=True)  # New field to store job_id from XML
    title = models.CharField(max_length=255)
    description = models.TextField()
    employer = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    date_posted = models.DateTimeField()
    promoted = models.BooleanField(default=False)
    apply_url = models.URLField(max_length=200)
    salary = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    reference_id = models.CharField(max_length=16, default=create_reference_id, unique=True)  # Corrected the indentation

    def __str__(self):
        return self.title
        

class Narrative(models.Model):
    text = models.TextField()
    processed_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
