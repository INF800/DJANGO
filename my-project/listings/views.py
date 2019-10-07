from django.shortcuts import render

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
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')