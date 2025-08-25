import pandas as pd
import json

#Leemos el archivo CSV
df = pd.read_csv('movies_initial.csv')

#Guardamos el DataFrame como JSON
df.to_json('movies.json', orient='records') #con orient=records indicamos que se debe guardar cada fila del DataFrame como un registro en el archivo JSON

with open('movies.json','r') as file: #abrimos el archivo movies.json en modo lectura (r)
    movies= json.load(file) #cargaos el contenido del json en la var movies, usando json.load, así movies será una lista de diccionarios

for i in range(100):
    movie = movies[i]
    print(movie)
    break

