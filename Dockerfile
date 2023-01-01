# CONSTS
ARG PYTHON_VERSION=3.10.4
ARG SHA256=f8cc89f5e47347703ec0c2b755464d7db2fa16f255ab860c4b24ba6ef2402020


############    BUILD Stage    ############
FROM python:${PYTHON_VERSION}-slim AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y

WORKDIR /usr/app
COPY requirements.txt .
RUN pip install --target=/usr/app/modules -r requirements.txt


############    PROD Stage    ############
FROM python:${PYTHON_VERSION}-slim@sha256:${SHA256} AS prod

RUN groupadd -g 999 python && useradd -r -u 999 -g python python

RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

COPY --chown=python:python --from=build /usr/app/modules ./modules
COPY --chown=python:python ./src/ ./src/
COPY --chown=python:python main.py .

USER 999

ENV PYTHONPATH="${PYTHONPATH}:/usr/app/modules"
CMD ["python", "main.py"]