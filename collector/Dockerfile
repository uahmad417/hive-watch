FROM python:alpine3.20

RUN apk update

WORKDIR /collector

COPY requirements.txt ./
COPY collector.py ./

RUN pip3 install -r requirements.txt

ENV SYSLOG_HOST=0.0.0.0
ENV SYSLOG_PORT=5170
ENV PYTHONUNBUFFERED=1ssh

CMD [ "python3", "collector.py" ]