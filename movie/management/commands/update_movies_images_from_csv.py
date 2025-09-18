import os
import csv
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images in the database from a CSV file"

    def handle(self, *args, **kwargs):

        # ✅ Fetch all movies from the database
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies") #Comando para imprimirpro consola desde un comando.

        # ✅ Process each movie
        for movie in movies:
           
            try:
                self.stdout.write(f"Processing: {movie.title}")
                new_image_path = f"movie/images/m_{movie.title}.png"
                movie.image = new_image_path
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))
                
            except Movie.DoesNotExist:
                self.stderr.write(f"Movie not found: {movie.title}")
            except Exception as e:
                self.stderr.write(f"Failed to update {movie.title}: {str(e)}")

        # ✅ Al finalizar, muestra cuántas películas se actualizaron
        self.stdout.write(self.style.SUCCESS(f"Finished updating all movies images from CSV."))
