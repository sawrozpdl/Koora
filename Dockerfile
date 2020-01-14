FROM python:latest
RUN mkdir koora
RUN mkdir requirements
WORKDIR /koora
COPY requirements ./requirements
RUN pip install -r requirements/production.txt
COPY . .
WORKDIR /koora/src/
RUN chmod +x /koora/script/runserver.sh
CMD ["/koora/script/runserver.sh"]