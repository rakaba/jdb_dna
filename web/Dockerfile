FROM python:3.7.3-alpine

WORKDIR tsumiage/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache build-base mariadb-connector-c-dev

RUN pip install --upgrade pip


RUN apk add --update \
            udev \
            ttf-freefont \
            chromium \
            openssl \
            chromium-chromedriver \
            gfortran \
            gcc \
            g++





COPY Pipfile Pipfile.lock ./
RUN pip install pipenv \
 && pipenv install --system

COPY . ./
CMD ["gunicorn", "-c", "gunicorn.conf", "jdbpj.wsgi", "-t", "15000"]