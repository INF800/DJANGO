# import get_object_or_404 along with render
from django.shortcuts import render, get_object_or_404

#import Paginator
from django.core.paginator import Paginator

# import listing model for fetching
from .models import Listings



def index(request):
    # This will fetch all listings without any raw sql queries
    # minus in '-list_date' is for descending order
    listings = Listings.objects.order_by('-list_date').filter(is_published=True)

    # right underneath listings objects', do as said in docs
    paginator = Paginator(listings, 6) # Show 25 contacts per page
    page = request.GET.get('page') # `page` is the url param we are looking for
    paged_listings = paginator.get_page(page) # pass this into context instead of `listings`

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):

    # we are fetching listinG (singular) from db
    # instead of using Listings.obects... we use
    # get_object_or_404() what it does is,
    # If i go to listings/10 even if '10' doesn't exist, i dont get 404. This adds 404 page
    # it takes 2 inputs: model and a primary key (pk)
    # pk helps in getting exact object from db
    listing = get_object_or_404(Listings, pk=listing_id) # listing_id comes from params of def listing() which in turn was passed from urls.py


    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

def search(request):
    return render(request, 'listings/search.html')