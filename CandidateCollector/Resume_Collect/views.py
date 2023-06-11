from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import *
from .forms import *
from .utils import *

@unauthenticated_user
def Register(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Collection')

    context = {'form': form}
    return render(request, 'Resume_Collect/Register.html', context)

@unauthenticated_user
def Access(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Collection')
            else:
                messages.error(request, 'Incorrect username or password')

    context = {'form': form}
    return render(request, 'Resume_Collect/Access.html', context)

@login_required(login_url='Access')
def Collection(request):
    active_user = request.user
    if 'opening' not in request.POST:
        openingform = OpeningForm(request.POST or None)
    if 'candidate' not in request.POST:
        candidateform = CandidateForm(request.POST or None, request.FILES or None, user=active_user)
    if 'search' not in request.POST:
        searchform = SearchForm(request.POST or None, user=active_user)
    query = None
    if request.method == 'POST':
        if 'opening' in request.POST:
            openingform = OpeningForm(request.POST)
            if openingform.is_valid():
                name = openingform.cleaned_data['name']
                if Opening.objects.filter(name=name, user=active_user).exists():
                    openingform.add_error('name', 'Job Opening already exists.')
                else:
                    opening = openingform.save(commit=False)
                    opening.user = active_user
                    request.session['opening_id'] = str(opening.id)
                    request.session['opening_name'] = str(opening.name)
                    candidateform = CandidateForm(initial={'opening': opening.id}, files=None)
                    searchform = SearchForm(initial={'opening': opening.id})
                    openingform = OpeningForm(initial={'name': None})
                    opening.save()
                    candidateform = CandidateForm(initial={'opening': opening.id}, user=active_user, files=None)
                    searchform = SearchForm(initial={'opening': opening.id}, user=active_user)
                    openingform = OpeningForm(initial={'name': None})

        if 'candidate' in request.POST:
            candidateform = CandidateForm(request.POST, request.FILES, user=active_user)
            if candidateform.is_valid():
                opening = candidateform.cleaned_data.get('opening')
                request.session['opening_id'] = str(opening.id)
                request.session['opening_name'] = str(opening.name)
                for f in request.FILES.getlist('resumes'):
                    text = read_pdf(f)
                    text = remove_null_bytes(text)
                    candidate = extract_candidate(text)
                    Candidate.objects.create(
                        opening=opening,
                        resume=f,
                        name=candidate['name'],
                        phone=candidate['phone'],
                        email=candidate['email'],
                        education=candidate['education'],
                        experience=candidate['experience'],
                        text_list=candidate['text_list'],
                        user=active_user
                    )


        if 'search' in request.POST:
            searchform = SearchForm(request.POST, user=active_user)
            if searchform.is_valid():
                query = searchform.cleaned_data.get('query')
                opening = searchform.cleaned_data.get('opening')
                if opening:
                    request.session['opening_id'] = str(opening.id)
                    request.session['opening_name'] = str(opening.name)
                    candidateform = CandidateForm(initial={'opening': opening.id}, user=active_user, files=None)
                    searchform = SearchForm(initial={'opening': opening.id, 'query': query}, user=active_user)
                else:
                    request.session['opening_id'] = None
                    request.session['opening_name'] = 'All Candidates'
                    searchform = SearchForm(initial={'query': query}, user=active_user)

        if 'delete_candidate' in request.POST:
            candidate_id = request.POST.get('delete_candidate')
            candidate = get_object_or_404(Candidate, id=candidate_id)
            request.session['opening_id'] = str(candidate.opening.id)
            request.session['opening_name'] = str(candidate.opening.name)
            candidateform = CandidateForm(initial={'opening': candidate.opening.id}, user=active_user, files=None)
            searchform = SearchForm(initial={'opening': candidate.opening.id}, user=active_user)
            candidate.delete()

        if 'delete_opening' in request.POST:
            opening_id = request.session.get('opening_id')
            if opening_id:
                opening = get_object_or_404(Opening, id=opening_id)
                opening.delete()
                request.session['opening_id'] = None
                request.session['opening_name'] = None

    opening_id = request.session.get('opening_id')
    opening_name = request.session.get('opening_name')



    if opening_id:
        candidates = Candidate.objects.filter(opening__id=opening_id)
    else:
        opening_name = 'All Candidates'
        candidates = Candidate.objects.filter(user=active_user)
        if len(candidates) == 0:
            opening_name = None

    if query:
        keywords = [word.strip() for word in query.split('&')]
        print(query)
        for keyword in keywords:
            candidates = candidates.filter(text_list__icontains=keyword)
    else:
        query = None

    opening = Opening.objects.filter(id=opening_id)

    if request.method == 'GET':
        candidateform = CandidateForm(initial={'opening': opening_id}, user=active_user, files=None)
        searchform = SearchForm(initial={'opening': opening_id}, user=active_user)

    total_candidates = candidates.count()

    context = {
        'candidates': candidates, 
        'opening': opening,
        'total_candidates': total_candidates, 
        'openingform': openingform, 
        'candidateform': candidateform,
        'opening_name': opening_name,
        'searchform': searchform,
        'query': query
    }

    return render(request, 'Resume_Collect/Collection.html', context)


def Resume(request, pk):
    candidate = Candidate.objects.get(id=pk)
    return render(request, 'Resume_Collect/Resume.html', {'candidate':candidate})

def Exit(request):
    logout(request)
    return redirect('Access')


"""NEW IDEA: ADD A FORM FOR JOB DESCRIPTION IN OPENING MODEL, RECRUITERS WILL COPY PASTE THEIR JOB DESCRIPTION TO IT,
THEN WHEN CANDIDATES ARE ADDED THE CANDIDATE THAT MATCHES THE JOB DESCRIPTION MOST WILL BE ORDERED FROM HIGHEST TO LOWEST
BASED ON A SCORE THAT IS CREATED BY COMPARING ALL THE WORDS CONTAINED IN THE DESCRIPTION WITH tHE TEXT LIST OF THE CANDIATE... But HOW ???
NOT ANOTHER FOR LOOP PLEASE D:"""
