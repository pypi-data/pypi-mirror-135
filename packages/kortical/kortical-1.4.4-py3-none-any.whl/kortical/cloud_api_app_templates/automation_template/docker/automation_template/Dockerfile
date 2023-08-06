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
ADD . /data/automation_template
ADD docker/automation_template/run-cmd.sh /usr/local/bin/run-cmd.sh

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=$HOME/.cache/pip --mount=type=ssh \
    apt-get update && \
    apt-get install ssh -y && \
    mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts && \
    apt-get install gcc git git-core -y && \
    . /opt/kortical-cloud/venvs/app-venv/bin/activate && \
    pip install cryptography==2.9 gitpython==3.1.24 gitdb==4.0.7 setuptools==51.1.1 && \
    pip install -r /data/requirements.txt && \
    pip install /data/automation_template && \
    apt-get purge -y --auto-remove gcc

FROM python:3.8-slim

RUN groupadd korticalgroup && \
    useradd -ms /bin/bash kortical -g korticalgroup

COPY --from=compile --chown=kortical:korticalgroup /data/automation_template/src /data/automation_template/src/
COPY --from=compile --chown=kortical:korticalgroup /opt/kortical-cloud/venvs/app-venv /opt/kortical-cloud/venvs/app-venv/
COPY --from=compile --chown=kortical:korticalgroup /usr/local/bin/run-cmd.sh /usr/local/bin/run-cmd.sh

RUN chmod +x /usr/local/bin/run-cmd.sh

USER kortical