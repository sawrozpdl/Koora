# This Dockerfile is meant to be used for production only!
# For development, use the one in directory: /dockerfiles

FROM python:latest
RUN mkdir code
RUN mkdir requirements
RUN mkdir scripts
COPY requirements /requirements
COPY src /code
COPY script /scripts
RUN chmod +x /scripts/runserver.sh
RUN pip install -r requirements/production.txt
WORKDIR /code
CMD ["/scripts/runserver.sh"]