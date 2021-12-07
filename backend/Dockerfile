FROM python:3.9-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /src

RUN pip install poetry
COPY pyproject.toml* poetry.lock* ./
RUN poetry export --without-hashes --dev -o requirements-dev.txt

RUN pip install --upgrade pip && pip install -r requirements-dev.txt --no-cache-dir

WORKDIR /src/backend