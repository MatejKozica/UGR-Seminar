FROM python:3.8-slim

WORKDIR /app

COPY pyproject.toml /app/

RUN apt-get update && apt-get install git -y &&\
    pip install --upgrade pip

COPY . /app
RUN pip install -e .

EXPOSE 8000
