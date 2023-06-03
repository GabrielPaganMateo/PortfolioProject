from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from .utils import *
import io

def LogIn(request):
    return render(request, 'Resume_Collect/LogIn.html')

def Collection(request):
    openingform = OpeningForm(request.POST or None)
    candidateform = CandidateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if 'opening' in request.POST:
            openingform = OpeningForm(request.POST)
            if openingform.is_valid():
                name = openingform.cleaned_data['name']
                print(name)
                if Opening.objects.filter(name=name).exists():
                    print("HELLOO")
                    openingform.add_error('name', 'Job Opening already exists.')
                else:
                    opening = openingform.save() 
                    request.session['opening_id'] = str(opening.id)
                    request.session['opening_name'] = str(opening.name)
                    return redirect('/Collection')
        if 'candidate' in request.POST: # <<< This returns True
            candidateform = CandidateForm(request.POST, request.FILES)
            if candidateform.is_valid():
                opening = candidateform.cleaned_data.get('opening')
                request.session['opening_id'] = str(opening.id)
                request.session['opening_name'] = str(opening.name)
                for f in request.FILES.getlist('resumes'):
                    text = read_pdf(f)
                    text = remove_null_bytes(text)
                    Candidate.objects.create(
                        opening=opening,
                        resume=f,
                        name=extract_name(text),
                        phone=extract_phone(text),
                        email=extract_email(text),
                        education=extract_education(text),
                        experience=extract_experience(text),
                        text_list=list_text(text),
                    )
                """candidateform.save()
                #text = read_pdf(request.FILES['resume'])
                #createCandidate(text, request.FILES['resume'])"""
                return redirect('/Collection')

    opening_id = request.session.get('opening_id')
    opening_name = request.session.get('opening_name')

    if opening_id:
        candidates = Candidate.objects.filter(opening__id=opening_id)
    else:
        candidates = Candidate.objects.none() 
    total_candidates = candidates.count()

    return render(request, 'Resume_Collect/Collection.html', {'candidates':candidates, 'total_candidates':total_candidates, 'openingform':openingform, 'candidateform':candidateform, 'opening_name':opening_name})

def Resume(request, pk):
    candidate = Candidate.objects.get(id=pk)
    return render(request, 'Resume_Collect/Resume.html', {'candidate':candidate})
