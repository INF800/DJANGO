# 01. Install and setup docke

In command prompt, `docker` command should work

# 02. Create repo in github

- add *python* `.gitignore` while creating repo
- clone repo in local machine
- cd to the cloned folder and `code .` or `atom .`

# 03. Create Dockerfile
 
 *A file that contains a list of instructions for docker to build our docker image. (i.e it contains dependancies)*

- At root directory create a file named `Dockerfile`

- The first line of the docker file is the image that you're going to inherit your docker file from. 

*basically build images on top of other images. you can find an image that has pretty much everything that you need for your project and then you can just add the customized bits that you need.*

Goto hub.docker.com -> search python -> alpine 3.7 -> redirected to github (use as reference)

```
FROM alpine:3.9
MAINTAINER Asapanna Rakesh

ENV PYTHONUNBUFFERED 1
```

`ENV PYTHONUNBUFFERED 1` is recommended wheneverr using python

- Install dependencies from requirements.txt

```
FROM alpine:3.9
MAINTAINER Asapanna Rakesh

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
```

`COPY ./requirements.txt /requirements.txt` : Copies requirements.txt from local machine to docker image

- Create directory in docker image to store our sourcecode and switch to it as default directory.

- copy sourcecode

```
FROM alpine:3.9
MAINTAINER Asapanna Rakesh

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
```
(Note: `/` means local machine and `./` means docker image location)

- Create user to run our applications and switch to that user (Vulnerability avoidance)

```
FROM alpine:3.9
MAINTAINER Asapanna Rakesh

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
```

- save this file.

# 04. Create requirements file

- check latest versiion of packages at https://pypi.org/

```
Django>=2.2.6,<=2.3.0
djangorestframework>=3.10.0,<3.11.0
```
`>=2.2.6,<=2.3.0` installs latest releases like security patches without abrupt changes.


- **Create empty folder `app` which will be copied to docker image**

# 05. Open command prompt in root dir

`docker build .`

*Builds dockerfile in root dir. As fast as your image weight*

Outputs: `sucessfully built`

# 06. Create docker-compose configutration

*It is a tool that allows us to run docker image easily form our project location and manage different services like pyhon and database*

- create `docker-compose.yml` in root dir. It conatains configuration for all the services that make up ourr project.

- we are using version 3

```
version: "3"

services:
    app:
        build:
            context: .
```
We are going to have a service called `app `and in `build` section of the configuration we are setting `context` to `.` i.e our current dir

- expose our port `host-port: docker-image-port`
- `volumes` updates our project into docker in real time automatically. `local-dir : docker-image-dir ` 
- `command` runs our application in docker container. 
    - `sh`: Shell
    - `-c`: Command

```
version: "3"

services:
    app:
        build:
         context: .
        ports:
         - "8000:8000"
        volumes:
         - ./app:app
        command: >
         sh -c "python manage.py runserver 0.0.0.0:8000"
```

`sh -c "python manage.py runserver 0.0.0.0:8000"` will run Django development server on all available ip addresses in docker container on port `8000`

- Save the file.

# 07. Build image using docker-compose configuration

- Open command prompt in root dir
`docker-compose build`

Outputs: 

`sucessfully built <id>`

`sucessfully tagged name-of-the-project`

(speed depends on image)


# 08. Build Django projects using django-compose built previouly

[PROJECTS BUILDING STARTS HERE]

- Create project files that we need for our app

- Goto command prompt root dir and type 
"docker-compose run name-of-the-service-in-yml-config-file command-in-linux-container"

`docker-compose run app sh -c "django-admin.py startproject app ."`

(Creates in "WORKDIR")