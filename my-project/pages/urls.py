# just like urls.py in projname folder. For 'path'
from django.urls import path

# import views to bind to
from . import views

# as in urls.py in projname folder
# '' meaans index unlike '/' in flask
# access view func from views.py
# name='index' helps associatre name to the path
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
]