FROM python:3.7-alpine

LABEL description="This container serves as an entry point for our future Django projects."

# Developed for Werbeagentur Christian Aichner by Florian Kleber
# for terms of use have a look at the LICENSE file.
MAINTAINER Florian Kleber <kleberbaum@erebos.xyz>

# Add custom environment variables needed by Django or your settings file here:
ENV DJANGO_DEBUG=on \
    DJANGO_SETTINGS_MODULE=esite.settings.production

# The uWSGI configuration (customize as needed):
ENV UWSGI_VIRTUALENV=/venv \
    UWSGI_UID=1000 \
    UWSGI_GID=2000 \
    UWSGI_WSGI_FILE=esite/wsgi_production.py \
    UWSGI_HTTP=:8000 \
    UWSGI_MASTER=1 \
    UWSGI_WORKERS=2 \
    UWSGI_THREADS=1

WORKDIR /code/

# Add pre-installation requirements:
ADD requirements/ /requirements/

# Update, install and cleaning:
RUN echo "## Installing base ##" && \
    echo "@main http://dl-cdn.alpinelinux.org/alpine/edge/main/" >> /etc/apk/repositories && \
    echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing/" >> /etc/apk/repositories && \
    echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community/" >> /etc/apk/repositories && \
    apk upgrade --update-cache --available && \
    \
    apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    make \
    libc-dev \
    musl-dev \
    libffi-dev \
    linux-headers \
    pcre-dev \
    postgresql-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    expat-dev \
    ;\
    apk add --force \
    git@main \
    bash@main \
    libjpeg-turbo@main \
    pcre@main \
    ffmpeg@main \
    postgresql-client@main \
    tini@community \
    \
    && python -m venv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install -r /requirements/production.txt" \
    && runDeps="$( \
    scanelf --needed --nobanner --recursive /venv \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | sort -u \
    | xargs -r apk info --installed \
    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps \
    && rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/*

EXPOSE 8000

VOLUME /code/media

ADD . /code/

# Place init, make it executable and
# make sure venv files can be used by uWSGI process:
RUN mv /code/docker-entrypoint.sh / ;\
    chmod +x /docker-entrypoint.sh ;\
    find /venv/ -type f -iname "*.py" -exec chmod -v +x {} ;\
    \
    # Call collectstatic with dummy environment variables:
    DATABASE_URL=postgres://none REDIS_URL=none /venv/bin/python manage.py collectstatic --noinput

# I personally like to start my containers with tini
# which start uWSGI, using a wrapper script to allow us to easily add
# more commands to container startup:
ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]

CMD ["/venv/bin/uwsgi", "--http-auto-chunked", \
    "--http-keepalive", \
    "--static-map", \
    "/media/=/code/media/"\
    ]

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
