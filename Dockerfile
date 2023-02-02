FROM python:3.11.1-alpine3.17

WORKDIR /api

COPY requirements.txt .
COPY requirements.dev.txt .

RUN python -m venv /venv && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev linux-headers && \
    apk add --update --no-cache postgresql-client && \
    /venv/bin/pip install -r requirements.txt && \
    /venv/bin/pip install -r requirements.dev.txt

RUN mkdir -p /vol/media && \
    mkdir -p /vol/static_files/static
    # im not sure about 777 here, should be 755?

COPY . /api

ENV PATH="/venv/bin:$PATH"
