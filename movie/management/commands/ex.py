import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Obtain embeddings for all movies using OpenAI embeddings"

    def handle(self, *args, **kwargs):        

        # Obtain, for each movie, their embedding
        movies = Movie.objects.all()
        for movie in movies:
            print("movie",movie," emb= ", movie.emb)
            print("----")

