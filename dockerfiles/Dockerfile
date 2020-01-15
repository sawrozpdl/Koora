# This Dockerfile is meant to be used for development only!
# For production, use the one in the base directory

FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir code
RUN mkdir requirements
RUN mkdir scripts
COPY requirements /requirements
COPY src /code
COPY script /scripts
RUN chmod +x /scripts/runserver.sh
RUN chmod +x /scripts/test.sh
RUN pip install -r /requirements/development.txt
WORKDIR /code
EXPOSE 8000