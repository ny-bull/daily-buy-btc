FROM python:3.10-buster

RUN mkdir src
WORKDIR /src

COPY . .

RUN pip install -r requirements.txt 