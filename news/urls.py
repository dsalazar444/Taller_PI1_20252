#Como es la URL de una app, se debe crear este archivo manualmente
from django.urls import path
from . import views #Importamos el archivo views ubicado en esta carpeta (news), por eso el .
#Se debe importar views porque las rutas ue definimos acá deben ser congruentes
#con las funciones creadas en views.py

urlpatterns = [
    path('', views.news, name='news'), #redirigimos las solicitud a la vista de noticias
    # views.news es la funcion en views que se ejecuta cuando se accede a la url
    # y con el name definimos un nombre unico para esa RUTA
]