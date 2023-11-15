FROM python:3.10-slim
WORKDIR /url_shortener
ENV POETRY_VERSION=1.5.1 \
    PATH="/root/.local/bin:$PATH" \
    PYTHONPATH="/url_shortener"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN mkdir -p /url_shortener/src && \
    touch /url_shortener/src/__init__.py && \
    touch /url_shortener/README.md

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false  && \
    poetry install

COPY src/app/ ./src/app/

ENTRYPOINT ["python3", "src/app/main.py"]