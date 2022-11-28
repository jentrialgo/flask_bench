FROM grafana/k6
FROM python:3.11.0-alpine

COPY --from=0 /usr/bin/k6 /usr/bin
COPY run.py /
COPY load.js /

RUN pip3 install click

ENV SERVER "localhost"

ENTRYPOINT ["sh", "-c", "python run.py --server=${SERVER}"]
