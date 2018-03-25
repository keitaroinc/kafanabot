FROM alpine:3.6

LABEL author="AtanasK"

RUN apk add --update \
              ca-certificates \
              musl \
              build-base \
              python3 \
              python3-dev \
              bash \
              git \
              gfortran \
              lapack-dev \
              libxml2-dev \
              libxslt-dev \
              jpeg-dev \
              nginx \
              uwsgi \
              uwsgi-python3 \
              curl \
 && pip3.6 install --upgrade pip \
 && rm /var/cache/apk/*

RUN echo "manylinux1_compatible = True" > /usr/lib/python3.6/_manylinux.py \
 && cd /usr/bin \
 && ln -sf easy_install-3.6 easy_install \
 && ln -sf idle3.6 idle \
 && ln -sf pydoc3.6 pydoc \
 && ln -sf python3.6 python \
 && ln -sf python-config3.6 python-config \
 && ln -sf pip3.6 pip \
 && ln -sf /usr/include/locale.h /usr/include/xlocale.h

RUN mkdir /app \
 && chown -R nginx:nginx /app \
 && chmod 777 /run/ -R \
 && chmod 777 /root/ -R


ADD . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt

EXPOSE 5000

ENV FLASK_APP ./app.py
ENV FLASK_DEBUG 1
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

COPY nginx.conf /etc/nginx/nginx.conf
COPY app.ini /app.ini

HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1

#CMD python app.py
CMD nginx && uwsgi --ini /app.ini
