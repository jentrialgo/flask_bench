FROM python:3.11.0-alpine

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

ARG secret_key
ENV SECRET_KEY $secret_key

COPY . /app
WORKDIR /app

RUN chmod +x gunicorn.sh

ENTRYPOINT ["./gunicorn.sh"]
