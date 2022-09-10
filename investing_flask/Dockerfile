FROM python:3.9.14-slim-buster




# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt


RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /usr/src/app/


ENV FLASK_APP /usr/src/app/investing_flask/manage.py

