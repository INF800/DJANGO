# import get_object_or_404 along with render
from django.shortcuts import render, get_object_or_404

#import Paginator
from django.core.paginator import Paginator

# import listing model for fetching
from .models import Listings

#import dictionaries from choices.py
from .choices import price_choices, bedroom_choices, state_choices


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

    # get all listings just like listings page
    queryset_list = Listings.objects.order_by('-list_date')
    # Now, add filters based on search

    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    
    # state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
     
    
    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list
    }
    return render(request, 'listings/search.html', context)