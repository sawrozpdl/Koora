FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir koora
RUN mkdir requirements
WORKDIR /koora
COPY requirements ./requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /koora/src/
EXPOSE 8000