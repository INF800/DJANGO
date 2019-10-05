from django.urls import path

from . import views

urlpatterns = [
    # calls index method of listings app view. 
    # '' corresponds to '/listings`
    path('', views.index, name='listings'),

    # parameter for single listing eg. 'listings/23'
    path('<int:listing_id>', views.listing, name='about'),

    # search. 
    # url must be 'listings/search'
    # note: we didn't add 'listings' in path url below 'search' 
    # as we will be doing it in main urls.py by linking to it. 
    path('search', views.search, name='search'),
]