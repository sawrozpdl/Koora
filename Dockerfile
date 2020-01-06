FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /koora
COPY requirements.txt /koora/
RUN pip install -r requirements.txt
COPY . /koora
WORKDIR /koora/src
EXPOSE 8000