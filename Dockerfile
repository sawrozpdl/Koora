FROM python:latest
RUN mkdir koora
RUN mkdir requirements
WORKDIR /koora
COPY requirements ./requirements
RUN pip install -r requirements/production.txt
COPY . .
WORKDIR /koora/src/
RUN python manage.py migrate
RUN python manage.py runserver $PORT