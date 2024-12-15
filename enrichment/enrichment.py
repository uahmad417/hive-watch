import logging

import requests
import os

from paho.mqtt import client as mqtt
import json


class Enrichment:
    """
    Represents the enrcihment service

    ## Attributes


    """

    def __init__(self) -> None:
        self.logger: logging.Logger = self.create_logger()
        self.subscriber: mqtt.Client = None

    def start(self):
        """
        start the enrichment service by starting the broker subscriber
        """

        broker_host = os.getenv("MQTT_HOST")
        broker_port = os.getenv("MQTT_PORT")
    
        self.subscriber = self.create_mqtt_subscriber()
        self.subscriber.connect(broker_host, int(broker_port))
        self.subscriber.loop_forever()

    def create_logger(self) -> logging.Logger:
        """
        Setup and configure the logger for this module

        ## Returns

        configured logger object for this module
        """

        logger = logging.Logger(__name__)
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)
        formatter = logging.Formatter(
            fmt="{asctime} - {name} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )
        console_handler.setFormatter(formatter)
        logger.setLevel(os.environ.get("LOGGING_LEVEL"))
        logger.info("Starting Enrichment service...")
        return logger

    def create_mqtt_subscriber(self) -> mqtt.Client:
        """
        Configure the mqtt subscriber

        ## Returns

        A `mqtt.Client` object
        """

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.tls_set("ca.crt")
        client.tls_insecure_set(True)
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message

        return client

    def __on_connect(self, client, userdata, flags, reason_code, properties):
        """
        When connected with the broker then subscribe to the topic
        """

        if reason_code.is_failure:
            self.logger.error(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        else:
            self.logger.info(f"Connected with broker")
            self.subscriber.subscribe("cowrie/#")

    def __on_message(self, client, userdata, message):
        """
        When message is recieved, perform enrichemnt
        """

        # self.logger.info(f"Recieved data: {message.payload.decode('utf-8')}")
        # self.logger.info(f"Recieved data: {json.loads(message.payload.decode('utf-8'))}")
        decoded_data = json.loads(message.payload.decode("utf-8"))
        self.check_ip(decoded_data)

    def check_ip(self, data):

        src_ip = data.get("data").get("src_ip")
        self.logger.info(src_ip)
        if src_ip:
            response = requests.get(
                url="https://api.abuseipdb.com/api/v2/check",
                params={"maxAgeInDays": 90, "ipAddress": src_ip},
                headers={"Key": os.environ.get("ABUSEIPDB_API_KEY"), "accept": "application/json"}
                )
            self.logger.info({response.content})