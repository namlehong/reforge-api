FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN set -ex \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "reforge.asgi:application"]