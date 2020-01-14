FROM python:latest
RUN mkdir koora
RUN mkdir requirements
WORKDIR /koora
COPY requirements ./requirements
RUN pip install -r requirements/production.txt
COPY . .
WORKDIR /koora/src/
CMD ["python manage.py migrate ; python manage.py runserver $PORT"]