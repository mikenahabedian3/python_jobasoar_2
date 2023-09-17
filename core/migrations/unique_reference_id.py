from django.db import migrations
from django.utils.crypto import get_random_string

def generate_unique_reference_ids(apps, schema_editor):
    Job = apps.get_model('core', 'Job')
    jobs = Job.objects.all()
    
    for job in jobs:
        job.reference_id = get_random_string(length=16)
        job.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_job_job_id_job_id_job_xml_job_id'),
    ]

    operations = [
        migrations.RunPython(generate_unique_reference_ids),
    ]
