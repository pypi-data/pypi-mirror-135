FROM python:3.8-slim

RUN apt-get update -y --allow-releaseinfo-change && apt-get install -y git gcc python3-dev && pip install setuptools

COPY . /mailutility
WORKDIR /mailutility/
RUN pip install -r requirements.txt && pip install .
WORKDIR /
RUN rm -rf mailutility
