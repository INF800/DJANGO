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