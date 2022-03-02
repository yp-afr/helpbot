FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip3 install -r requirements.txt
COPY . /src