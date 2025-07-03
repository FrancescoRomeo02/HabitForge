FROM python:3.13-slim-bullseye

WORKDIR /backend
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
 
# install system dependencies
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install netcat gcc postgresql-client libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
 
# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt

# Download spaCy models
RUN python -m spacy download it_core_news_sm
RUN python -m spacy download en_core_web_sm
 
# Copy application code
COPY . /backend

# Create a script to wait for database
RUN echo '#!/bin/bash\n\
set -e\n\
host="$1"\n\
port="$2"\n\
shift 2\n\
cmd="$@"\n\
\n\
until nc -z $host $port; do\n\
  >&2 echo "Database is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
\n\
>&2 echo "Database is up - executing command"\n\
exec $cmd' > /backend/wait-for-db.sh && chmod +x /backend/wait-for-db.sh

# Set the working directory for the application
WORKDIR /backend

# Expose port
EXPOSE 8000