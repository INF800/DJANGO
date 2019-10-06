`pip3 freeze` shows packages installed in global scope

# Create virtual env

run `python3 -m venv ./venv` in proj folder
 
*You'll see a folder named venv created in root dir. If it doesnt work try python instead of python 3 when having python 3 in global scope. elase put absolute path c://*

# Activate venv
`./ven/Scripts/activate.bat`

*check using pip freeze*

# Deactiave venv

`deactivate`

# Install Django

`pip install django`

`pip freeze`

*To create django project we use a special CLI program called django-admin*

`django-admin help`

- create project

`django-admin startproject projectname .`

*This will also create manage.py, tool we will use*

`python manage.py`


# Create Django .gitignore

- Goto gitignore.io -> Django Python
- Paste in `.gitignore` in child foder but correct one. Works!
- add `venv` in the end of .gitignore file


# Run development server

`python manage.py runserver` runs dev server

*Note: db.sqlite3 will be generated on running the server. We will not be developing in sqlite because it is good for dev and prototyping but not production( large data and large traffic).*


# Exploring initial files

`__init.py__` 

    - Always empty to begin with
    - Not goiint to touch it or use it. Ignore

`settings.py`

    Bunch of key-value pairs

    - BASE_DIR: Base directory
    - SECRET_KEY: For production
    - DEBUG: True/Flase. In production, set to Flase
    - ALLOWED_HOSTS: Empty array at first, but when deployed, list of host domains added
    - INSTALED_APPS: We can have multiple apps for a project which will take care of each task.
    - MIDDLEWARE: CRF and all security based
    - ROOT_URLCONF: string representing full import path. It is where initial url file will be. projname.url
    - TEMPLATES: htmls to display. Where to look for templates and what options to look for.
    - WSGI_APPLICATION: Path of wsgi application object that django's builting servers use. Note "wsgi.py" file
    - DATABASES: Set up db params. Change it to postgres
    - AUTH_PASSWORD_VALIDATORS: Where we set types of rules for our passwords
    - STATIC_URL: Path we wanna use for static files

`urls.py`

    - Kind of like routing file (collection of all app urls and links)
    - path should have fwd slash at the end
    - paths are linked to view method or urls form another file
    eg. when we create a new app called 'listings', it will create a new folder by that name. We have to create new 'urls.py' in that app folder

`wsgi.py`

    - web server gateway interface
    - specifiation that describes how a web server communicates with web application and how can web apps be changed.
    - Has to do a lot about hosting a site.


# Creating first app in django

*We are going to have multiple apps per project*

- Create pages app
    - displays homepage, about page or any other static page
- we can import models into pages app so that we can display data

In terminal: `python manage.py startapp pages`

*creates a "pages" folder in root dir*

`__init__.py`

    - Completely empty as before. Ignore

`migrations`

    - For any db migrations we create

`admin.py`

    - Use if you want to show stuff in admin area

`apps.py`

    - shows class of the PagesConfig (in settings file)

`models.py`

    - we create models here (data)

`tests.py`

    - To run any tests

`views.py`

    - used to create methods and link urls to them


**ADD THIS NEW APP TO `SETTINGS` IN `PROJNAME` FOLDER**

djangoapp/settings.py
```
INSTALLED_APPS = [
    'pages.apps.PagesConfig', 
]
```
*This makes django to recognoze newly created app*

- From venv, install autopep8 for formating: `pip install autopep8`

- create `urls.py` inside pages app folder

pages/urls.py
```
# just like urls.py in projname folder. For 'path'
from django.urls import path

# import views to bind to
from . import views

# as in urls.py in projname folder
# '' meaans index unlike '/' in flask
# access view func from views.py
# name='index' helps associatre name to the path
urlpatterns = [
    path('', view.index, name='index'),
]
```

pages/views.py
```
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# index view (called by urls)
def index(request):
    return HttpResponse('<h1>Heloo </h1>')
```

still not done, goto main urls.py and link the `pages/url.py` using `path('', include('pages.urls')),`


djangoprojecy/urls.py:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
]

```

Check browser for output.

*(Install pylint in venv like autopep8 to avoid import errors)*


# Serving html TEMPLATE instead of returning simple `HttpResponse`

- Steps to be followed

- tell django where to look for templates (folder). Goto `djangoapp/settings.py`

```
TEMPLATES = 
...
'DIRS' = [os.path.join(BASE_DIR, 'templates')]
...

```

- create `templates` folder in root for of project *you can organize files in the folder in whichever way you want*

- [ ME ]create `pages` folder for all templates for that app. inside, i.`index.html` ii.`about.html`

templates/pages/index.html
```
<H1> HOME </H1>
```
templates/pages/about.html
```
<H1>ABOUT</H1>
```

- As templates are created, add path for `about` in `pages/urls.py`
```
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
```
- add about in `pages/views.py` and replace `HttpResponse` with `render`
```
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# index view (called by urls)
def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html;')
```

`render()` takes request self as one argument and template as another.

**CHECK OUTPUT IN BROWSER**

# Extend a BASE layout so that scripts and stylesheets dont gahve to be put for each template separately (Not SPA)

- create `base.html` inside `templates/`:  (! + tab for boilerplate code)

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    {% block content %} {% endblock %}
</body>
</html>
```
Jinja syntax is used

- to use `base.html` in `index.html` and `about.html`:

templates/pages/index.html:
```
{% extends 'base.html' %}

{% block content %}
<H1>HOME</H1>
{% endblock %}
```
templates/pages/about.html
```
{% extends 'base.html' %}

{% block content %}
<H1>ABOUT</H1>
{% endblock %}
```

**View in browser and verify by viewing sourcecode**

(*Install jinja extension for vs code as well as python extension*)

# Implementing bootstrap theme 

**HANDLING STATIC FILES:** *Confusing. Fpollow along carefully.*

- Goto projname, `djangoproject` folder amd create folder `static`. *This is where we put our main static files*

- put `css` `js` `webfonts` and `img` inn that folder

-  goto `djangoproject/settings.py` (bottom)

``` 
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    # location of static folder we just created in djangoproject/
    os.path.join(BASE_DIR, 'dangoproject/static')
]
```
`STATIC_ROOT`: When you deploy your application, you run command called `collectstatic`. It goest into all your apps and if they have a static folder, it takes everything out and puts it into root `static` folder.

- run `python manage.py collectstatic`: *You will see that  a new `static` folder pops up in rroot dir with nt only the static files we created but inbuilt ones*

**Note:** There is a typo. `dangoapp` instead of djangoapp

Outputs: 

```
150 static files copied to 'C:\Users\user\Desktop\github\DJANGO\my-project\static'.
```

- add `/static` to `.gitignore`

# Load bootstrap

- In head, we include our static files. Take it from themes folder and paste in `templates/base.html`

- Javascript files may be there in our theme jus above ending of body tag, copythem aswell.

- correct the src href addresses for static files

check: `templates/base.html`
```
{% load static %}
<!DOCTYPE html>
.
.
.
<link ... href="{% static 'css/all.css' %}">
.
.
.
```

- add headers, footers and navbars from theme
    - Add `templates/partials` folder to put all these imported html code so that `base.html` is not cluttered.
    - Syntax (folder):
    ```
    templates/
        partitals/
            _navbar.html
            _topbar.html
            _footer.html
        base.html
    ```
    Simply cut paste in respective partial html files and call them in `base.html` using template syntax
    ```
    <!-- Top Bar-->
    {% include 'partials/_topbar.html' %}
    ```

**NOTE:** Always check errors in console and analyze and correct them

# COPY SPECIFIC MARKUPS INTO `index.html` and `about.html` from static files and themes

- dont worry about file not found errors for image assets. They will not come from static files. db will be used

templates/pages/about.html
```
{% extends 'base.html' %}

<!--'load' always below 'extends' -->
{% load static %}

```

- Replace all occurances of 
```
<a href="index.html">
```
with
```
 <a href="{% url 'index' %}">
```

The url `'index'` comes from `pages/urls.py/` file's `name='index'`

- You can use jinja template for dynamic behaviour
eg. templates/paartials/_navbar.html
```
                  <li 
                    {% if '/' == request.path %}
                      class="nav-item active mr-3"
                    {% else %}
                      class="nav-item mr-3"
                    {% endif %}
                  >
```
Here, `{% if '/' == request.path %}` chhecks for homepage
```
                  <li 
                    {% if 'about' in request.path %}
                      class="nav-item active mr-3"
                    {% else %}
                      class="nav-item mr-3"
                    {% endif %}
                  >
```
Here, `{% if 'about' in request.path %}` checks for about page



**NOTE:** This is more like realworld. first create ui then apply backend with django. Thats good approach.

# Create two more apps 
1. Listings
2. Realtors

- In terminal:
```
 python manage.py startapp listings
 python manage.py startapp realators
``` 

- Add to apps settings.py
```
INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'listings.apps.ListingsConfig',
    'realators.apps.RealatorsConfig',
]
```
*For `listings` we obviously have pages - single listing page, search page etc. But `realtors` is just for model (We are not oing to have any templates/views in it)*

- Add listings templates
    - create folder `templates/listings`
    - in that folder:
    - `listing.html`: For single lsitings
    - `listings.html`: list of listings
    - `seach.html`: to search

- As there will be urls to connect to, create `listings/urls.py`
```
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
```

- link to main `urls.py` same as pages app
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('listings/', include('listings.urls')),
    path('admin/', admin.site.urls),
]
```

Note: How `listings/` is used in main url instead of using in listings app 

- Create view methods in `lsitings/views.py`
```
from django.shortcuts import render

def index(request):
    return render(request, 'listings/listings.html')

def listing(request):
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')
```

*for now, put `<h1>listings<h1>` in all 3 templates then try visiting in browser at `127.0.0.1/listings/`*

- extend base.html
- copy static files into templates
- images wont be displayed as we will be displaying it when admin uploads it


# PostgreSQL Installation

- very powerful rdb
- pairs very well with djano
-no raw sql queries. High level ORM availsble

> postgresql.org -> download -> windows -> graphical installer by bigsql

> Mac: Use postgresapp.com

> pgadmin: gives gui (available at pgadmin.org for win + mac

- install with gui installer
- double click on `postgres` open a terminal window
- Post gres comes with def user `postgres`. We will use it in development but not deployment
    
    ```
    //add psql to envt vars

    >> psql -U postgres
    
    output: postgres=#
    ```
    - set password for `postgres` user
    ```
    \password postgres
    ```
    - Create db
    ```
    CREATE DATABASE dangoproject OWNER postgres;
    ```
    - list databases to see the created db
    ```
    \l
    ```
- you can use pgadmin agui to do above steps as well


- pgadmin
    - install and open
    - below left side pannel 'browser1, left click `servers`, `create`, `new...` 
    ```
    name: dbserver

    connection ->
    Host: localhhost
    maintenance db: postgres
    Username: postgres
    password: postgres

    save->
    ```
    - goto: servers -> dbserver -> Databases -> dangoproject(leftclick) -> properties -> security -> privilleges -> add grantee: postgres, select all

    **All set and configured**

# Django-Postgres setup

- install pip packages and define `settings.py`
    - in venv
    ```
    pip install psycopg2
    pip install psycopg2-binary
    ```
    dangoapp/seetings.py
    ```
    # Database

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            # name of db we created
            'NAME': 'dangoproject',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost'
        }
    }

    ```

    ***migration is a file that tells db what to do**. Basicall setting up tables, data, cols, datatypes etc.. Django has def migrations for things like admin area for authentication. All those migrartion files have been set up but havent been run and put into thedb. Hence the migration errors while running startup. Lets add those migrations to db...*

    - Run migrations that are already ready:
    ```
    python manage.py migrate
    ``` 
    Outsputs error if any error in our db setup.

    - You can see the created tables by migration in pgadmin
    > severs->dbserver->Databases->dangoapp->Schemas->public->Tables

    - run there sever
    ```
    python manage.py runserver
    ```
    *You wont be able to see all those migration errors you saw previously. We are in a great place now. We can actually create models!*


# Plan the schema before stating model creation

- It is always a good practice to map out db schema before we start coding
- Figure it out through project requirements
```
--->MODEL/DB FEILDS

### LISTING

-->feilds

id: INT     
(every TABLE has it. Automated in postgres)

realator INT (FOREIGN KEY [realator])    
(everly listing will have a realator. Hence assign a group of listings to a arealator. we can do it using: `realator-feild INT (FOREIGN KEY [realator-model])`)

title: STR
address: STR
city: STR
state: STR
zipcode: STR
description: TEXT (Longer than STR)
price: int (rounding houses price. Not doing cents!)
bedrooms: INT
bathrooms: INT
garage: INT [0] (default zero)
sqft: INT
lot_size: FLOAT (Acres hence float)
is_published: BOOL [true] (by default, published)
list_date: DATE

phot_main: STR (One main imaage. WE ARE NOT STORING IMAGES, RATHER LOCATION OF IMAGE)

photo_1: STR
photo_2: STR
photo_3: STR
photo_4: STR
photo_5: STR
photo_6: STR



### REALATORS

-->feilds

id: INT
name: STR
photo: STR
descripttion: TEXT
email: STR
phone: STR
is_mvp: BOOL [0] (Realator of the month)
hire_date: DATE



### CONTACT (for storing enquiries)

--> Feilds

id: INT
user_id: INT (to know which user enquired)
listing: INT (connected to tiltle/name of listing)
listing_id: INT
name: STR
email: STR
phone: STR
message: TEXT
contact_date: DATE

```

# CREATE MODELS AND UPDATE DB

- i. Create listings model
- ii. Create realators model
- iii. Run migration that will create tables in our db based on our models

*check django docs for all model feild types https://docs.djangoproject.com/en/2.2/ref/models/fields/*


***Note:** Use email field if available instead of ussing str feild and reinventing the wheel*

- Creating listings model:

listings/models.py
```
from django.db import models
from datetime import datetime

#we can access any APP by just using it's name
from realators.models import Realator

# Create your models here.

class Listings(models.Model):
    # hardest one
    # feild = models.ForeignKey(other-model-we-are-relating, on_delete=)
    # If you have realator attached to a listing, and you delete realator, should the listing delete too? In some cases we want it to. Here, Not needed
    realator = models.ForeignKey(Realator, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True) #blank=True mean it is optional. Same as 'Required' tag
    price = models.IntgerField()
    bedrooms = models.IntgerField()
    bathrooms = models.DecimalFeild(max_didgts=2, decimal_places=1)
    garage = models.IntgerField(default=0)
    sqft = models.IntgerField()
    lot_size = models.DecimalFeild(max_digits=5, decimal_places=1)
    # note: we are using actual images her, but in db itself, images will be stored as strings
    # photo_main = models.ImageFeild( define-where-to-upload-images-to-inside-MEDIA-FOLDER )
    # use string ormater to upload images neatly as per dates 
    photo_main = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/')
    photo_1 = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_2 = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_3 = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_4 = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_5 = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    photo_6 = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/', blank=True)
    is_published = models.BooleanFeild(default=True)
    list_date = models.DateTimeFeild(default=datetime.now, blank=True)

    # In admin area, we will have a table that diplays each listing. And we need
    # to pick main feild to be displayed there. "Tile" can be selected as main feild to display.
    def __str__():
        return self.title
```
- creating Realators model. It has to go hand in hand with previous model we created.
    - realators foreign key in listings model must linked
    - imports should match

realators/models.py
```
from django.db import models
from datetime import datetime

# Create your models here.

class Realator(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageFeild(upload_to='photos/%Y/%m/%m/%d/')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeFeild(default=datetime.now, blank=True)
    def __str__():
        return self.nmae
```

- Now, we want this to get into our db. *Just because we created models, it doesnt mean tables will be created itself*
    - create migrations
    ```
    python manage.py makemigrations
    ```
    `makemigrations` create a file which should be run to update db. It itself doesnt act on db

    *Note:* In apps folders, `migrations` folders should be already present

    If any erors, typos, install the dependancies.. solve them
    ```
    pip install Pillow
    ```
    when `makemigrations` get executed successfully, it creates `migrations\0001_initial.py` in all APPS. *This file basically contais all the info from our models which will be updated in db*

    We can actually know what sql quieries will be used using command:
    ```
    // syntax: python manage.py sqlmigrate appname NUMoFfile
    python manage.py sqlmigrate listings 0001
    ```
    *This command simply shows us queries. Dont implement it. You can see only if you want to*

    - run migration
    ```
    python manage.py migrate
    ```
    Take look in schemas->table in pgadmin to see changes.
    *You can view or edit tables by left clicking on it and selecting `View/Edt Data`*