FROM python:3.9.5-alpine

RUN apk add gcc linux-headers make libffi-dev musl-dev g++

RUN mkdir /app
WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv
RUN pipenv install