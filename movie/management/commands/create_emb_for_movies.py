import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv
from movie.utils import get_embedding

class Command(BaseCommand):
    help = "Obtain embeddings for all movies using OpenAI embeddings"

    def handle(self, *args, **kwargs):
        # ✅ Load OpenAI API key
        load_dotenv('./openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # Obtain, for each movie, their embedding
        movies = Movie.objects.all()
        for movie in movies:
            emb = get_embedding(movie.description)
            #Convert array to list, because it is the emb type 
            movie.emb = emb.tolist() 
            movie.save()

