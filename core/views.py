from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import XMLUploadForm, parse_xml
from .models import Job

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard instead of home
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def upload_xml(request):
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            parse_xml(request.FILES['xml_file'])
            return redirect('job_list')
    else:
        form = XMLUploadForm()
    return render(request, 'core/upload_xml.html', {'form': form})

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'core/job_list.html', {'jobs': jobs})

def job_detail(request, reference_id):
    job = get_object_or_404(Job, reference_id=reference_id)
    return render(request, 'core/job_detail.html', {'job': job})
