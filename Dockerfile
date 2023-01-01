ARG PYTHON_VERSION=3.10.4
ARG SHA256=f8cc89f5e47347703ec0c2b755464d7db2fa16f255ab860c4b24ba6ef2402020

### Build ###
FROM python:${PYTHON_VERSION}-slim AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt



############    PROD Stage    ############
FROM python:${PYTHON_VERSION}-slim@sha256:${SHA256} AS prod

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

COPY --chown=python:python --from=build /usr/app/venv ./venv
COPY --chown=python:python ./src/ ./src/
COPY --chown=python:python .main.py .

USER 999

ENV PATH="/usr/app/venv/bin:$PATH"

CMD ["sh", "-c", "source .env && python ./main"]



############    DEV Stage    ############
# FROM python:${PYTHON_VERSION}-slim@sha256:${SHA256} AS dev

# RUN groupadd -g 999 python && \
#     useradd -r -u 999 -g python python

# RUN mkdir /usr/app && chown python:python /usr/app
# WORKDIR /usr/app

# COPY --chown=python:python requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# USER 999

# CMD ["sh", "-c", "uvicorn app:app --reload --host ${BACKEND_HOST} --port ${PORT}"]