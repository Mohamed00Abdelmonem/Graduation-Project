from django.shortcuts import render
from .models import Settings
# Create your views here.



def home(request):
    return render(request, 'index.html')