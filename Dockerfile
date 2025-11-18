# Stage 1

FROM python:3.14-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache build-base postgresql-dev

COPY pyproject.toml poetry.lock /app/
RUN pip install --upgrade pip && \
  pip install poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-root --no-interaction --no-ansi

# Stage 2

FROM python:3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser --disabled-password mp-user && \
  apk add --no-cache postgresql-client

COPY --from=builder --chown=mp-user:mp-user /usr/local/lib/python3.14/site-packages/ /usr/local/lib/python3.14/site-packages/
COPY --from=builder --chown=mp-user:mp-user /usr/local/bin/ /usr/local/bin/
COPY --chown=mp-user:mp-user . /app/

USER mp-user

EXPOSE 8000
