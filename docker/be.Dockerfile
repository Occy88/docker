FROM python:3.12-slim AS pythonbase

ARG POETRY_GROUPS
WORKDIR /app

RUN pip install --no-cache-dir poetry &&  poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --with web${POETRY_GROUPS:+,$POETRY_GROUPS}

FROM octo_base AS final
COPY --from=pythonbase /app /app
WORKDIR /app
COPY . /app
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--access-logfile", "-", "--workers", "4", "--bind", ":8000"]