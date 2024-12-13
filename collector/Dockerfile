FROM python:alpine3.20

RUN apk update

WORKDIR /collector

COPY requirements.txt ./
COPY collector.py ./
COPY __init__.py ./
COPY main.py ./

RUN pip3 install -r requirements.txt

ENV SYSLOG_HOST=0.0.0.0
ENV SYSLOG_PORT=5170
ENV LOGGING_LEVEL=INFO
ENV PYTHONUNBUFFERED=1

CMD [ "python3", "main.py" ]