from django.contrib import admin

# Register your models here.

from .models import Listings

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realator')
    list_display_links = ('id', 'title')
    # when you have single value inside parentheses like this, put coma in end else we get error
    list_filter = ('realator',)
    list_editable= ('is_published', 'realator')
    search_fields = ('title', 'description', 'city', 'address', 'price')
    list_per_page = 25

admin.site.register(Listings, ListingAdmin)