FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt

RUN groupadd -g 777 appuser && \
    useradd -r -u 777 -g appuser appuser
USER appuser

COPY . /code/
