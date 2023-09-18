from django import forms
import xml.etree.ElementTree as ET
from django.db import transaction
from django.utils.dateparse import parse_datetime
from .models import Job, Company

class XMLUploadForm(forms.Form):
    xml_file = forms.FileField()
    company = forms.ModelChoiceField(queryset=Company.objects.all())

@transaction.atomic
def parse_xml(xml_file, company):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for job in root.findall('job'):
            xml_job_id = job.find('job_id').text  # get job_id from XML
            title = job.find('title').text
            description = job.find('description').text

            location = job.find('location').text
            date_posted = parse_datetime(job.find('datePosted').text)
            promoted = job.find('promoted').text.lower() == 'true'
            apply_url = job.find('applyUrl').text
            salary = job.find('salary').text if job.find('salary') is not None else None
            job_type = job.find('jobType').text

            Job.objects.create(
                xml_job_id=xml_job_id,  
                title=title,
                description=description,
                employer=company,  # Use the company parameter here
                location=location,
                date_posted=date_posted,
                promoted=promoted,
                apply_url=apply_url,
                salary=salary,
                job_type=job_type,
            )
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        # Replace print statements with proper logging in the future
    except Exception as e:
        print(f"An error occurred: {e}")
        # Replace print statements with proper logging in the future
