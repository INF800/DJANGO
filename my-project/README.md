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
