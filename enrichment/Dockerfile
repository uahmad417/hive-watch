FROM python:alpine3.20

RUN apk update

WORKDIR /enrichment

COPY requirements.txt ./
COPY enrichment.py ./
COPY __init__.py ./
COPY main.py ./
COPY ca.crt ./

RUN pip3 install -r requirements.txt

ENV MQTT_HOST=localhost
ENV MQTT_PORT=443
ENV LOGGING_LEVEL=INFO
ENV PYTHONUNBUFFERED=1

CMD [ "python3", "main.py" ]