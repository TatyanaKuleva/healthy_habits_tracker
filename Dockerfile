FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /code

RUN pip install poetry==2.1.3

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root --only main

COPY . .

RUN useradd -m celeryuser
USER celeryuser

