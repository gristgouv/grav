FROM ghcr.io/astral-sh/uv:0.7-alpine AS requirements

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN uv export --no-dev --locked > requirements.txt

FROM python:3.13-alpine

WORKDIR /app

COPY --from=requirements /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src src

ENV UVICORN_PORT=80
ENV UVICORN_HOST=0.0.0.0

ENTRYPOINT [ "uvicorn","src.grav.app:app" ]

