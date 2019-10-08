from django.shortcuts import render
from django.http import HttpResponse

#import listings model
from listings.models import Listings
#import realators nodel
from realators.models import Realator

#import dictionaries from choices.py
from listings.choices import price_choices, bedroom_choices, state_choices


# index view (called by urls)
def index(request):
    
    # [:3] allows fetches only 3 listings from db
    listings = Listings.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }

    return render(request, 'pages/index.html', context)

def about(request):
    # Get all realators
    realators = Realator.objects.order_by('-hire_date')

    # Get MVP i.e seller(s) of the month
    mvp_realators = Realator.objects.all().filter(is_mvp=True)

    context = {
        'realators': realators,
        'mvp_realators': mvp_realators
    }

    return render(request, 'pages/about.html', context)