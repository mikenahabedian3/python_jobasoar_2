from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse

from .forms import XMLUploadForm, parse_xml, JobSeekerNarrativeForm
from .models import Job, Company
from .gpt3_setup import process_narrative

from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def receive_narrative(request):
    if request.method == "POST":
        narrative_text = request.POST.get('narrative_text')
        # Here, you will later add code to send the narrative_text to the GPT-4 for processing
        return JsonResponse({'message': 'Narrative received'})
    else:
        return JsonResponse({'message': 'Wrong request method'}, status=400)



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
            company = form.cleaned_data.get('company')
            parse_xml(request.FILES['xml_file'], company)
            return redirect('job_list')
    else:
        form = XMLUploadForm()

    companies_with_jobs = Company.objects.annotate(job_count=models.Count('job'))

    return render(request, 'core/upload_xml.html', {'form': form, 'companies_with_jobs': companies_with_jobs})

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'core/job_list.html', {'jobs': jobs})

def job_detail(request, reference_id):
    job = get_object_or_404(Job, reference_id=reference_id)
    return render(request, 'core/job_detail.html', {'job': job})

def process_narrative_view(request):
    if request.method == 'POST':
        narrative_text = request.POST.get('narrative_text', '')
        embeddings = process_narrative(narrative_text)
        response_data = {
            'embeddings_shape': embeddings.shape
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
