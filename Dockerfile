# Creating a python base with environment variables
FROM --platform=linux/amd64 python:3.10.3-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    WORKDIR=/code \
    VENV_PATH=/code/.venv

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder` stage is used to build deps + create our virtual environment
FROM base as builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install poetry
ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $WORKDIR
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev


FROM base as development

# Copying poetry and venv into image
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $WORKDIR $WORKDIR

WORKDIR $WORKDIR
# Runtime deps already installed. we install dev deps quickly
RUN poetry install
COPY ./app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


FROM base as production
COPY --from=builder $WORKDIR/.venv $WORKDIR/.venv

WORKDIR $WORKDIR
COPY ./app ./app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
