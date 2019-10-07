from django.shortcuts import render

# import listing model for fetching
from .models import Listings

def index(request):
    # This will fetch all listings without any raw sql queries
    listings = Listings.objects.all()

    context = {
        'listings': listings
    }

    return render(request, 'listings/listings.html', context)

def listing(request):
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')