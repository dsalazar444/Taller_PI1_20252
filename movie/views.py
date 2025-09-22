from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib 
import io
import numpy as np
import urllib, base64
from movie.utils import get_embedding, cosine_similarity

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page.</h1><h2>Daniela Salazar
    #Amaya</h2>')
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies= Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm,'movies': movies})

def recommendations(request):
    #Obtenemos input
    prompt = request.GET.get('searchMovieRecommendations')
    # Si no hay prompt (página cargada por primera vez), no llamamos a la API
    if not prompt or not prompt.strip():
        # mostrar la plantilla para que el usuario escriba en el cajón
        return render(request, 'recommendations.html', {'movies': [], 'searchTerm': 'None'})
   
    #Si sí tenemos prompt (clickearon Buscar), Obtenemos el emb del input
    
    # Generar embedding del prompt
    prompt_emb = get_embedding(prompt)

    # Recorrer la base de datos y comparar
    best_movie = None
    max_similarity = -1

    for movie in Movie.objects.all():
        movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
        similarity = cosine_similarity(prompt_emb, movie_emb)

        if similarity > max_similarity:
            max_similarity = similarity
            best_movie = movie

    #print(f"La película más similar al prompt es: {best_movie.title} con similitud {max_similarity:.4f}")
    return render(request, 'recommendations.html',{'movie':best_movie,'searchTerm':prompt,'max_similarity':f"{max_similarity:.4f}"})


def about(request):
    #return HttpResponse('<h1>Welcome to About page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    graphic_year = statistics_year()
    graphic_genre = statistics_genre()

    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})

def statistics_year():

    matplotlib.use('Agg') #Establecemos el backend de matplotlib en 'Agg', con el cual podemos generar graficos sin necesidad de una interfaz gráfica
    #years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') #Obtenemos todos losaños de las peliculas en la BD
    
    #Obtenemos todas las peliculas
    all_movies = Movie.objects.all()
    
    #Diccionario para almacenar cantidad de peliculas por año
    movie_counts_by_years= {}

    for movie in all_movies:
        year = movie.year if movie.year else "None" #Guardamos lo que haya en movie.year, si lo hay, sino "none"
        if year in movie_counts_by_years:
             movie_counts_by_years[year] += 1
        else:
            movie_counts_by_years[year] = 1 #Lo añadimos a la biblioteca, y le contamos la primera aparición

    #Ancho de las barras
    bar_width = 0.5
    #Posiciones de las barras
    bar_positions = range(len(movie_counts_by_years))

    #Creamos grafica de barras
    plt.bar(bar_positions, movie_counts_by_years.values(), width=bar_width, align='center')

    #Personalizamos la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_years.keys(), rotation=90)

    #Ajustamos espaciado entre barras
    plt.subplots_adjust(bottom=0.3)

    # Guardamos la gráfica en un objeto BytesIO
    buffer = io.BytesIO() #Creamos un buffer que contendrá la representación binaria de la gráfica
    plt.savefig(buffer, format='png') #Guardamos la imagen en el buffer
    buffer.seek(0)
    plt.close()

    # Convertimos la grafia a base64
    image_png = buffer.getvalue() #recuperamos la imagen del buffer (que está en binario)
    buffer.close()
    graphic = base64.b64encode(image_png) #Codifica esos datos binarios a base64, que es una forma de representar datos binarios como texto.
    graphic = graphic.decode('utf-8') #Convierte el resultado base64 (que es bytes) a una cadena de texto.

    # No la renderizamos, sino que retornamos normal, porque esto lo llamaremos
    # desde una función "padre", que sí renderizaremos
    return graphic


def statistics_genre():
    matplotlib.use('Agg') #Establecemos el backend de matplotlib en 'Agg', con el cual podemos generar graficos sin necesidad de una interfaz gráfica
    #years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') #Obtenemos todos losaños de las peliculas en la BD
    
    #Obtenemos todas las peliculas
    all_movies = Movie.objects.all()
    
    #Diccionario para almacenar cantidad de peliculas por año
    movie_counts_by_genre= {}

    for movie in all_movies:
        genre = movie.genre.split(',')[0].strip() if movie.genre else "None" #Guardamos lo que haya en movie.year, si lo hay, sino "none"
        if genre in movie_counts_by_genre:
             movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1 #Lo añadimos a la biblioteca, y le contamos la primera aparición

    #Ancho de las barras
    bar_width = 0.5
    #Posiciones de las barras
    bar_positions = range(len(movie_counts_by_genre))

    #Creamos grafica de barras
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center', color='pink')

    #Personalizamos la gráfica
    plt.title('Movies per genre (first only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)

    #Ajustamos espaciado entre barras
    plt.subplots_adjust(bottom=0.3)

    # Guardamos la gráfica en un objeto BytesIO
    buffer = io.BytesIO() #Creamos un buffer que contendrá la representación binaria de la gráfica
    plt.savefig(buffer, format='png') #Guardamos la imagen en el buffer
    buffer.seek(0)
    plt.close()

    # Convertimos la grafia a base64
    image_png = buffer.getvalue() #recuperamos la imagen del buffer (que está en binario)
    buffer.close()
    graphic = base64.b64encode(image_png) #Codifica esos datos binarios a base64, que es una forma de representar datos binarios como texto.
    graphic = graphic.decode('utf-8') #Convierte el resultado base64 (que es bytes) a una cadena de texto.

    # No la renderizamos, sino que retornamos normal, porque esto lo llamaremos
    # desde una función "padre", que sí renderizaremos
    return graphic




