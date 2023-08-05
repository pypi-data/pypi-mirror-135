# Ensure the environment variable DATATEER_DEPLOY_KEY_PREFECT_LIB is set, or the build will fail
# docker build --build-arg DATATEER_DEPLOY_KEY_PREFECT_LIB . --tag <image>:<version>
# to update linux dependencies rather than use the cached ones, build with docker's --no-cache flag
# FROM python:3.8.3
FROM python:3.8.7-slim-buster

WORKDIR /datateer

RUN apt-get -yq update \
    && apt-get -yqq install ssh git  gcc
# python3-dev gcc gfortran musl-dev
# libc-dev build-essential

# If this env var is set, the "meltano install" command will use this connection string
ARG MELTANO_DATABASE_URI
ARG DATATEER_DEPLOY_KEY_PREFECT_LIB
RUN test -n "$DATATEER_DEPLOY_KEY_PREFECT_LIB"

# add SSH private key so we can install the python packages from private repos
RUN mkdir /root/.ssh \
    && echo "${DATATEER_DEPLOY_KEY_PREFECT_LIB}" > /root/.ssh/id_rsa \
    && chmod 600 /root/.ssh/id_rsa \
    && touch /root/.ssh/known_hosts \
    && ssh-keyscan github.com >> /root/.ssh/known_hosts

# dependencies and venvs
COPY requirements/requirements-meltano.txt /datateer/requirements/
RUN python -m venv venv/meltano \
    && chmod -R 766 venv/meltano/bin \
    && venv/meltano/bin/pip install -r requirements/requirements-meltano.txt

COPY requirements/requirements-dbt.txt /datateer/requirements/
RUN python -m venv venv/dbt \
    && chmod -R 766 venv/dbt/bin \
    && venv/dbt/bin/pip install -r requirements/requirements-dbt.txt


# copy the remaining files in last; these will change most often, so by separating this line from the rest, we save a lot of time during docker build by using cached layers from the above commands
COPY meltano.yml /datateer/
RUN venv/meltano/bin/meltano install
COPY dbt_project.yml packages.yml /datateer/
COPY .datateer /datateer/.datateer
COPY orchestration /datateer/orchestration
COPY dbt /datateer/dbt
COPY setup.py MANIFEST.in /datateer/
RUN pip install .

# putting this last because it seems to invalidate the build cache every time
# ENV PYTHONPATH "${{PYTHONPATH}}:/datateer"
