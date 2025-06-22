FROM python:3.13-slim-bullseye

WORKDIR /backend
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
 
# install system dependencies
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
 
# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download it_core_news_sm
RUN python -m spacy download en_core_web_sm

 
COPY . /backend