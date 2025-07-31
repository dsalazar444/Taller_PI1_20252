from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page.</h1><h2>Daniela Salazar
    #Amaya</h2>')
    return render(request, 'home.html', {'name':'Daniela Salazar Amaya'})

def about(request):
    return HttpResponse('<h1>Welcome to About page</h1>')