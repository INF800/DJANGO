from django.db import models
from datetime import datetime

#we can access any APP by just using it's name
from realators.models import Realator

# Create your models here.

class Listings(models.Model):
    # hardest one
    # field = models.ForeignKey(other-model-we-are-relating, on_delete=)
    # If you have realator attached to a listing, and you delete realator, should the listing delete too? In some cases we want it to. Here, Not needed
    realator = models.ForeignKey(Realator, on_delete=models.DO_NOTHING)
    title =  models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True) #blank=True mean it is optional. Same as 'Required' tag
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    # note: we are using actual images her, but in db itself, images will be stored as strings
    # photo_main = models.Imagefield( define-where-to-upload-images-to-inside-MEDIA-FOLDER )
    # use string ormater to upload images neatly as per dates 
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    # In admin area, we will have a table that diplays each listing. And we need
    # to pick main field to be displayed there. "Tile" can be selected as main field to display.
    def __str__(self):
        return self.title