FROM python:3.12-slim

ARG POETRY_GROUPS
WORKDIR /app/web

RUN pip install --no-cache-dir poetry &&  poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --with web${POETRY_GROUPS:+,$POETRY_GROUPS}
