FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade awscli
RUN pip install -r requirements.txt

RUN groupadd -g 777 appuser && \
    useradd -r -u 777 -g appuser appuser

COPY ./scripts/init-dynamodb.sh /init-dynamodb.sh
RUN sed -i 's/\r$//g' /init-dynamodb.sh
RUN chmod +x /init-dynamodb.sh

USER appuser

COPY . /code/
