from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import XMLUploadForm, JobSeekerNarrativeForm, parse_xml
from .models import Job, Company, Narrative

import spacy

nlp = spacy.load("en_core_web_sm")

@csrf_exempt
def receive_narrative(request):
    if request.method == "POST":
        narrative_text = request.POST.get('narrative_text')
        processed_narrative = process_narrative(narrative_text)
        new_narrative = Narrative(text=narrative_text, processed_text=processed_narrative)
        new_narrative.save()
        return JsonResponse({'message': 'Narrative received and saved', 'original_narrative': narrative_text, 'processed_narrative': processed_narrative})
    else:
        return JsonResponse({'message': 'Wrong request method'}, status=400)




def process_narrative(narrative):
    doc = nlp(narrative)

    # Create a list to store the processed elements of the narrative
    processed_elements = []

    # Identify and add named entities to the processed elements list
    for ent in doc.ents:
        if ent.label_ not in ["DATE", "PERCENT", "CARDINAL"]:
            processed_elements.append(ent.text)

    # Identify and add unique noun phrases to the processed elements, excluding certain words
    for chunk in doc.noun_chunks:
        non_stop_words_in_chunk = [token.text for token in chunk if not token.is_stop and not token.is_punct and not token.text.lower() in ('i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours')]
        
        if non_stop_words_in_chunk:
            processed_elements.append(" ".join(non_stop_words_in_chunk))

    # Combine the processed elements to form the final processed narrative
    processed_text = " ".join(set(processed_elements))

    return processed_text




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
        processed_text = process_narrative(narrative_text)
        response_data = {'processed_text': processed_text}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
