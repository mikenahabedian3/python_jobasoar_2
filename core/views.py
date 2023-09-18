from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models

from .forms import XMLUploadForm, parse_xml
from .models import Job, Company  # Importing Company model here

from .forms import JobSeekerNarrativeForm

def home(request):
    if request.method == "POST":
        form = JobSeekerNarrativeForm(request.POST)
        if form.is_valid():
            narrative = form.save()  # Removed user assignment here
            # ... (we would now proceed to match the narrative with jobs here in future steps)
            return redirect('dashboard')
    else:
        form = JobSeekerNarrativeForm()

    return render(request, 'home.html', {'form': form})


def home(request):
    if request.method == "POST":
        form = JobSeekerNarrativeForm(request.POST)
        if form.is_valid():
            narrative = form.save(commit=False)
            narrative.user = request.user
            narrative.save()
            return redirect('dashboard')
    else:
        form = JobSeekerNarrativeForm()

    return render(request, 'home.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def upload_xml(request):
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the selected company from the form
            company = form.cleaned_data.get('company')
            # Call the parse_xml function with the XML file and the company
            parse_xml(request.FILES['xml_file'], company)
            return redirect('job_list')
    else:
        form = XMLUploadForm()

    # Get a list of companies along with the count of jobs associated with them
    companies_with_jobs = Company.objects.annotate(job_count=models.Count('job'))

    return render(request, 'core/upload_xml.html', {'form': form, 'companies_with_jobs': companies_with_jobs})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'core/job_list.html', {'jobs': jobs})

def job_detail(request, reference_id):
    job = get_object_or_404(Job, reference_id=reference_id)
    return render(request, 'core/job_detail.html', {'job': job})
