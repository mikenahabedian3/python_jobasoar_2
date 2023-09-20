from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import XMLUploadForm, JobSeekerNarrativeForm, parse_xml
from .models import Job, Company, Narrative
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Initialize the GPT-2 model and tokenizer once to improve performance
model_name = "gpt2-medium"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def process_narrative(narrative):
    model_name = "gpt2-medium"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    
    inputs = tokenizer.encode(narrative, return_tensors='pt')
    outputs = model.generate(
        inputs, 
        max_length=150, 
        num_return_sequences=1, 
        temperature=0.5,
        no_repeat_ngram_size=2
    )
    processed_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return processed_text



@csrf_exempt
def receive_narrative(request):
    if request.method == "POST":
        narrative_text = request.POST.get('narrative_text')
        processed_narrative = process_narrative(narrative_text)
        new_narrative = Narrative(text=narrative_text, processed_text=processed_narrative)
        new_narrative.save()
        return JsonResponse({'message': 'Narrative received and saved', 'processed_narrative': processed_narrative})
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
        processed_text = process_narrative(narrative_text)
        response_data = {'processed_text': processed_text}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
