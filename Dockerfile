FROM python:3.7-alpine

WORKDIR /opt/task_queue

COPY requirements.txt requirements.txt
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3.7 install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY src src
ENV FLASK_APP=src/api/common.py

EXPOSE 5000

CMD flask run --host=0.0.0.0
