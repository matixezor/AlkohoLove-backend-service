FROM python:3.10.4-slim-buster
WORKDIR /src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /src