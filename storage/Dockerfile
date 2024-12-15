FROM python:alpine3.20

RUN apk update

WORKDIR /storage

COPY requirements.txt ./
COPY storage.py ./
COPY __init__.py ./
COPY main.py ./
COPY ca.crt ./

RUN pip3 install -r requirements.txt

ENV MQTT_HOST=localhost
ENV MQTT_PORT=443
ENV MQTT_TOPIC=enriched
ENV LOGGING_LEVEL=INFO
ENV ELASTIC_HOST=http://elastic:9092
ENV ELASTIC_INDEX=sensors
ENV PYTHONUNBUFFERED=1

CMD [ "python3", "main.py" ]