import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
import random


class Command(BaseCommand):
    help = "Obtain the embedding of a random movie"

#Crear el comando que permita visualizar los embeddings de una película seleccionada al azar. Entregable: Captura de pantalla de los embeddings.
    def handle(self, *args, **kwargs):
        # Obtener todos los IDs que realmente existen
        existing_ids = list(Movie.objects.values_list('id', flat=True))

        # Seleccionar un ID aleatorio de los que existen
        random_id = random.choice(existing_ids)
        
        # Obtener la película con ese ID (ahora sí existe)
        movie = Movie.objects.get(id=random_id)
        
        #Reestructuramos su embedding para que salga como vector
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
        print(movie.title, embedding_vector[:5])  # Muestra los primeros valores
