FROM python:3.12-slim as builder

LABEL authors="octavio@msk.ai"
# ENVIRONMENT CONFIGURATION
ARG USER_ID
ARG GROUP_ID
# create the appropriate directories
ENV APP_HOME=/home/app/web
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore


RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/staticfiles && mkdir -p $APP_HOME/media && mkdir -p $APP_HOME/logging


# INSTALL DEBIAN DEPS
RUN apt-get -y update && apt-get -y install \
    git \
    libpq-dev \
    gettext-base \
    python3


# USER & GROUP SETUP
RUN addgroup --system app && adduser --system app --ingroup app
RUN useradd -r -g app gunicorn && \
    useradd -r -g app worker && \
    useradd -r -g app flower && \
    git config --global --add safe.directory /app && \
    mkdir -p /home/app/.cache

# If USER_ID and GROUP_ID are provided, adjust the created user and group
RUN if [ -n "$USER_ID" ] && [ -n "$GROUP_ID" ]; then \
        usermod -u $USER_ID app && \
        groupmod -g $GROUP_ID app; \
    fi
RUN chown -R app:app $APP_HOME
RUN chmod -R u+rw $APP_HOME;
RUN chown -R app:app /home/app/.cache
# for pycharm skeleton updates...
RUN chown -R app:app /tmp

# DEP INSTALLATION
COPY docker/wait-for-it.sh /usr/bin/wait-for-it.sh
WORKDIR $APP_HOME
RUN git config --global --add safe.directory /app

ADD . $APP_HOME
USER app