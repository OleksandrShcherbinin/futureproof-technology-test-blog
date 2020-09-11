FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

RUN apt update

COPY requirements.txt /code/

RUN apt-get update && apt-get install -y gconf-service libasound2 \
    libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 \
    libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation \
    libappindicator1 libnss3 lsb-release xdg-utils libevent-dev

RUN apt-get install -y gettext

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
