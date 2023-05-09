from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def LogIn(request):
    return render(request, 'Resume_Collect/LogIn.html')

def Collection(request):
    return render(request, 'Resume_Collect/Collection.html')

