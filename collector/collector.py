import logging
import os
import socket

from paho.mqtt import client as mqtt


class Collector:
    """
    Represents the collector service

    ## Attributes

    producer (mqtt.Client): KafkaProducer instance to push data onto the broker

    sock (socket.socket): Socket instance to recieve logs from syslog server

    logger (logging.Logger): module level logger object
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = self.create_logger()
        self.producer: mqtt.Client = self.create_mqtt_producer()
        self.sock: socket.socket = None

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
        logger.info("Starting collector service...")
        return logger

    def create_mqtt_producer(self) -> mqtt.Client:
        """
        Configure the mqtt producer

        ## Returns

        A `mqtt.Client` object
        """

        broker_host = os.getenv("MQTT_HOST")
        broker_port = os.getenv("MQTT_PORT")
        client = mqtt.Client()
        client.tls_set("ca.crt")
        client.tls_insecure_set(True)
        client.on_connect = self.__on_connect
        client.on_publish = self.__on_publish
        client.connect(broker_host, int(broker_port))
        client.loop_start()
        return client

    def start(self) -> None:
        """
        Initialize and bind the socket
        """

        host = os.environ.get("SYSLOG_HOST")
        port = int(os.environ.get("SYSLOG_PORT"))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()

    def recieve_logs(self) -> None:
        """
        Continiously recieve logs from server
        """

        if not self.sock:
            raise RuntimeError("Socket is not initialized. Call start() first")

        try:
            while True:
                conn, addr = self.sock.accept()
                with conn:
                    self.logger.info(f"Connected by: {addr}")
                    data = conn.recv(4096)
                    if not data:
                        break
                    self.process_logs(data, addr)

        except KeyboardInterrupt:
            self.logger.info(f"Shutting down collector....")

        finally:
            self.close()

    def process_logs(self, log, addr) -> None:
        """
        Process the recieved logs

        ## Parameters

        log (str): Log recieved as string

        addr (str): server address from which log was recieved
        """

        # TODO: this should not be hardcoded
        self.logger.info(f"msg is {log}")
        self.producer.publish(topic="cowrie", payload=log, qos=0, retain=False)

    def close(self) -> None:
        """
        Close the socket connection gracefully
        """

        if self.sock:
            self.sock.close()
            self.sock = None

    def __on_connect(self, client, userdata, flags, reason_code):
        """
        When connected with mqtt broker
        """

        if reason_code == 0:
            self.logger.info(f"Connected with mqtt broker {reason_code}")
        else:
            self.logger.error(
                f"Failed to connect with broker with result: {reason_code}")

    def __on_publish(self, client, userdata, mid):
        """
        when messge is published to broker
        """

        self.logger.debug(f"Msg published {mid}")
