FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
COPY . /app
COPY ./entrypoint.sh /entrypoint.sh

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev && apk \
  add --no-cache python3-dev libxslt-dev libxml2-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

WORKDIR /app

#RUN mkdir -p /vol/web/media
RUN mkdir -p /app/static
RUN adduser -D user
RUN chown -R user:user /app/
RUN chmod -R 755 /app
RUN chown -R user:user /app/django_cache
RUN chmod -R 755 /app/django_cache

USER user

ENTRYPOINT [ "sh", "/entrypoint.sh" ]