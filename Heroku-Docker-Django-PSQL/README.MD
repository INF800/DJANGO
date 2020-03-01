## Deployment

#### 01. Docker Setup

Follow https://docs.docker.com/compose/django/ and test `postgres` image setup with `docker-compose up` (done in below steps)

- Write a `Dockerfile` in main dir with `requirements.txt`
    ```
    FROM python:3.6.8
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /code
    WORKDIR /code
    COPY requirements.txt /code/
    RUN pip install -r requirements.txt
    COPY . /code/
    ```
    requirements.txt
    ```
    Django>=2.0,<3.0
    psycopg2>=2.7,<3.0
    gunicorn // added for heroku
    django-heroku // added for heroku
    ```

- Write `docker-compose.yml` in main dir which will be used by CLI tool `docker-compose` for command `docker-compose up`

    ```
    version: '3'

    services:
    db:
        image: postgres
        restart: always
        environment:
        POSTGRES_PASSWORD: example
        ports:
        - "5432:5432" # why not working?
    web: # sudo docker-compose run web python manage.py shell
        restart: always
        build: .
        command: python manage.py runserver 0.0.0.0:8000 # add to `django->appname->settings.py->ALLOWED_HOSTS = ["0.0.0.0"]` 
        volumes:
        - .:/code
        ports:
        - "8000:8000"
        depends_on:
        - db
    ```
    
    - add `"0.0.0.0"` to 
        ```
        django->appname->settings.py->ALLOWED_HOSTS = ["0.0.0.0"]
        ``` 
    
    - Run `Sudo docker-compose run web python manage.py shell` locally to grab required python-django and postgres images from docker hub. Exit the shell
        ```
        # `sudo docker-compose run web python manage.py shell`
        #       Use this command right after `Dockerfile` and `docker-compose.yml` files are written. Downloads
        #       relevant images. 
        #       Note: 
        #         - You can give any python version as per your wish in Dockerfile `FROM python:3.6.8`
        #         - Can try any other command: eg. `sudo docker-compose run web <any-command>`
        #         - `web` is our `app` metioned in `docker-compose.yml`
        ```
    
    - setup postgres
        ```
        # 2. Setup postgresql: https://docs.docker.com/compose/django/
        #       - use postgresql (https://hub.docker.com/_/postgres [docker stack or docker-compose section])
        #       - pasword: example
        #       - username: postgres
        #       Note:
        #         - add password in `docker-compose.yml` `services->db->environment->POSTGRES_PASSWORD`
        #         - add password in django-project/settings.py/
        #           ```    
        #                DATABASES = {
        #                    'default': {
        #                        'ENGINE': 'django.db.backends.postgresql',
        #                        'NAME': 'postgres',
        #                        'USER': 'postgres',
        #                        'PASSWORD': 'example',
        #                        'HOST': 'db',
        #                        'PORT': 5432,
        #                    }
        #                }
        #           ```
        ```
    - run `docker-compose up`. If it the webpage is being served with no python/django/postgres errors, **all set!** You can spin up the entire local development environment with one command: `docker-compose up`
        ```
        # 3. `sudo docker-compose up`
        #       Wakes up a container based on `docker-compose.yml` in parent directory. (Run this command in
        #       parent directory where we have `docker-compose.yml`.)
        #       
        #   ->  According to this `docker-compose.yml` file, `sudo docker-compose up` will set up postgres database and
        #       serve the django website.
        ```
#### Now, Heroku Setup

- Make sure `docker-compose up` spins up entire dev environment locally
- Follow (https://devcenter.heroku.com/articles/django-app-configuration) done below –
    - Make `Procfile` in main dir
        ```
        web: gunicorn <django-project-name>.wsgi
        ```
        example,
        ```
        web: gunicorn Eather.wsgi
        ```
    - upload the sourcecode to *github-repo*
    - Create an `app` from heroku website
    - Note, `heroku-postgres` will be automatically attached to *Resources* of our heroku *app* as long as we use same *postgres* image (https://hub.docker.com/_/postgres)
    - Goto `Deploy`
        - Deployment method -> `Github`
        - Connect the *github-repo*
        - Enable Automatic Deploy
        - Mannual Deploy -> Master -> Deploy Branch
            - You should see a success message! with link to hosted site... 

- Install `heroku` CLI to view logs using simple one-line command. Add app flag `-a` to your appname eg. `-a project-eather`

- **Note**
    - This will perfectly work fine if you are `build`ing docker image for first time but,
    - when you are building it not for the first time, you will face issues as `django-heroku` and `gunicorn` might not be present in your docker image right from the start (Note: we are not at all using containers here)
    - To resolve the issue
        - in local main dir run `docker build .`
            - This will build the new docker image but won't be able to overwrite the old docker image. You will have to do it manually.
            - The newly created docker image will be named as `<none>` with almost same size as old image
            - Rename the old docker image to something else (remember it's actual name)
                - `docker tag <old_name> <new_name>` eg. `docker tag project-eather_web project-eather_web_old`
            - Rename the newly built docker image to the actual name of the old image
                - `docker tag <image-id-of-new-image> <actual-name-of-old-image>` eg. `docker tag 68227db0dc4b project-eather_web`
            - Remove the old image
                - `docker rmi <image-id> -f`
            - check
                - `docker-compose up`
    - Note: you can avoid all this by simply deleting the old image and building image afresh with new requirements.txt `docker build .`