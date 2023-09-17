from django import forms
import xml.etree.ElementTree as ET
from django.db import transaction
from django.utils.dateparse import parse_datetime
from .models import Job, Company


class XMLUploadForm(forms.Form):
    xml_file = forms.FileField()


@transaction.atomic
def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for job in root.findall('job'):
            title = job.find('title').text
            description = job.find('description').text
            employer_name = job.find('employer').text

            # Get or create the employer (Company)
            employer, created = Company.objects.get_or_create(name=employer_name)

            location = job.find('location').text
            date_posted = parse_datetime(job.find('datePosted').text)
            promoted = job.find('promoted').text.lower() == 'true'
            apply_url = job.find('applyUrl').text
            salary = job.find('salary').text if job.find('salary') is not None else None
            job_type = job.find('jobType').text

            Job.objects.create(
                title=title,
                description=description,
                employer=employer,
                location=location,
                date_posted=date_posted,
                promoted=promoted,
                apply_url=apply_url,
                salary=salary,
                job_type=job_type,
            )
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        # Ideally, replace print statements with proper logging
        # handle the XML parse error (perhaps raise a custom exception)
    except Exception as e:
        print(f"An error occurred: {e}")
        # handle other types of errors (perhaps raise a custom exception)
