from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import *
from .forms import OpeningForm, CandidateForm
from .utils import *

def LogIn(request):
    return render(request, 'Resume_Collect/LogIn.html')

def Collection(request):
    """openings = Opening.objects.all()"""
    candidates = Candidate.objects.all()
    total_candidates = candidates.count()
    openingform = OpeningForm()
    if request.method == 'POST':
        if 'opening' in request.POST:
            openingform = OpeningForm(request.POST)
            if openingform.is_valid():
                openingform.save()
                return redirect('/Collection')
            elif 'candidate' in request.POST:
                candidateform = CandidateForm(request.POST, request.FILES)
                print(candidateform)
                if candidateform.is_valid():
                    candidate = candidateform.save(commit=False)
                    text = extract_text_from_pdf(candidate.resume.path)
                    text = remove_null_bytes(text)
                    name = extract_name(text)
                    phone = extract_phone(text)
                    email = extract_email(text)
                    education = extract_education(text)
                    experience = extract_experience(text)
                    text_list = list_text(text)
                
                    candidate = Candidate.objects.create(
                        name=name,
                        phone=phone,
                        email=email,
                        education=education,
                        experience=experience,
                        text_list=text_list,
                        opening=opening_object,
                        resume=
                    )
                    candidate.save()
                    # Here you would typically add any additional processing, e.g. extracting info from resume.
                    # For now, we'll just save the instance.
                    candidate.save()
                    return redirect('/Collection')

    return render(request, 'Resume_Collect/Collection.html', {'candidates':candidates, 'total_candidates':total_candidates, 'openingform':openingform})

def AddOpening(request):
    openingform = OpeningForm()
    if request.method == 'POST':
        openingform = OpeningForm(request.POST)
        if openingform.is_valid():
            openingform.save()

    return render(request, 'Resume_Collect/Collection.html', {'candidates':candidates, 'total_candidates':total_candidates, 'openingform':openingform})

def Resume(request, pk):
    candidate = Candidate.objects.get(id=pk)
    return render(request, 'Resume_Collect/Resume.html', {'candidate':candidate})
