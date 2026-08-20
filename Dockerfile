FROM python:3.12-slim-trixie

ENV POETRY_VERSION=2.2.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN groupadd --gid 1000 user \
    && useradd --uid 1000 --gid user --create-home --shell /usr/sbin/nologin user \
    && mkdir -p "$POETRY_CACHE_DIR" && chown user:user "$POETRY_CACHE_DIR"

WORKDIR /app

COPY --chown=user:user . .
RUN chown user:user /app

USER user

RUN poetry install --no-interaction --no-cache --without dev

CMD [ "poetry", "run", "bot" ]
