FROM python:3.8-slim

WORKDIR /app

ENV PATH="/root/.local/bin:$PATH"
COPY poetry.lock pyproject.toml /app/

RUN apt-get update && apt-get install curl git -y && \
    # Install poetry
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.7.1 python3 - && \
    # Install barebones instead of in virtualenv
    poetry config virtualenvs.create false && \
    # Install deps
    poetry install --no-root --all-extras

COPY . /app
RUN poetry install

EXPOSE 8000