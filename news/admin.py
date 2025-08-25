from django.contrib import admin
from .models import News

# Register your models here.
#Cada que agreguemos nuevos modelos se debe usar python
# manage.py makemigrations y python manage.py migrate
admin.site.register(News)