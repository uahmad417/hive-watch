import json
import logging
import os

from elasticsearch import Elasticsearch
from paho.mqtt import client as mqtt


class Storage:
    """
    Represenets the storage service

    ## Attributes:

    """

    def __init__(self) -> None:
        self.logger: logging.Logger = self.create_logger()
        self.subscriber: mqtt.Client = None
        self.es_client: Elasticsearch = self.get_elastic_client()

    def start(self) -> None:
        """
        start the storage service.

        initializes the mosquitto subscriber to start consuming messages
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

    def get_elastic_client(self) -> Elasticsearch:
        """
        Create the elasticsearch client object
        """

        client = Elasticsearch(hosts=os.environ.get("ELASTIC_HOST"))
        self.logger.info(f"Connection to Elasticsearch established at {os.environ.get("ELASTIC_HOST")}")
        return client

    def create_mqtt_subscriber(self) -> mqtt.Client:
        """
        Configure the mqtt subscriber

        ## Returns

        A `mqtt.Client` object
        """

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.tls_set("ca.crt")
        client.tls_insecure_set(True)
        client.on_connect = self.__subscriber_on_connect
        client.on_message = self.__subscrber_on_message

        return client

    def __subscriber_on_connect(self, client, userdata, flags, reason_code, properties):
        """
        When connected with the broker then subscribe to the topic
        """

        if reason_code.is_failure:
            self.logger.error(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        else:
            self.logger.info(f"Subscriber connected with broker")
            self.subscriber.subscribe(f"{os.environ.get("MQTT_TOPIC")}/#")

    def __subscrber_on_message(self, client, userdata, message):
        """
        When message is recieved, perform enrichemnt
        """

        decoded_data = json.loads(message.payload.decode("utf-8"))
        self.upload_to_elastic(decoded_data)

    def upload_to_elastic(self, data) -> None:
        """
        Upload the data to elasticsearch
        """

        response = self.es_client.index(index=os.environ.get("ELASTIC_INDEX"), body=data)
        self.logger.debug(f"Document index to elasticsearch {response}")