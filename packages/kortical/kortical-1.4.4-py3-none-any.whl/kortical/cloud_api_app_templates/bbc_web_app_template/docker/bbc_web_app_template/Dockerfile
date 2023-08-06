# syntax=docker/dockerfile:experimental
FROM python:3.8-slim as compile

ENV LANG=en_GB.UTF-8
ENV LC_ALL=en_GB.UTF-8
ENV PYTHONUNBUFFERED=1

RUN python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools && \
    mkdir -p /opt/kortical-cloud/venvs && \
    python3 -m venv /opt/kortical-cloud/venvs/app-venv

ADD requirements.txt /data/requirements.txt
ADD . /data/bbc_web_app_template
ADD docker/bbc_web_app_template/run-cmd.sh /usr/local/bin/run-cmd.sh

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install dos2unix -y  && \
    find /data/bbc_web_app_template -type f -print0 | xargs -0 dos2unix -- && \
    dos2unix /usr/local/bin/run-cmd.sh && \
    dos2unix /data/requirements.txt && \
    apt-get purge -y --auto-remove dos2unix

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=$HOME/.cache/pip --mount=type=ssh \
    apt-get update && \
    apt-get install gcc -y && \
    . /opt/kortical-cloud/venvs/app-venv/bin/activate && \
    pip install -r /data/requirements.txt && \
    pip install /data/bbc_web_app_template && \
    apt-get purge -y --auto-remove gcc

FROM python:3.8-slim

RUN groupadd korticalgroup && \
    useradd -ms /bin/bash kortical -g korticalgroup

COPY --from=compile --chown=kortical:korticalgroup /data/bbc_web_app_template/src /data/bbc_web_app_template/src/
COPY --from=compile --chown=kortical:korticalgroup /opt/kortical-cloud/venvs/app-venv /opt/kortical-cloud/venvs/app-venv/
COPY --from=compile --chown=kortical:korticalgroup /usr/local/bin/run-cmd.sh /usr/local/bin/run-cmd.sh

RUN chmod +x /usr/local/bin/run-cmd.sh

USER kortical