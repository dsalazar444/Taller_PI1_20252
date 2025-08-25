from django.shortcuts import render
from .models import News

# Create your views here.
def news(request):
    newss = News.objects.all().order_by('-date') #indicamos que se ordenen los elementos de forma descendente (-) por fecha
    return render(request, 'news.html', {'newss':newss})