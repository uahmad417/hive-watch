import logging
import os
import socket

from kafka import KafkaProducer


class Collector:
    """
    Represents the collector service

    ## Attributes

    producer (KafkaProducer): KafkaProducer instance to push data onto the broker

    sock (socket.socket): Socket instance to recieve logs from syslog server

    logger (logging.Logger): module level logger object
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = self.create_logger()
        self.producer: KafkaProducer = self.create_kafka_producer()
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

    def create_kafka_producer(self) -> KafkaProducer:
        """
        Configure the kafka producer

        ## Returns

        A `KafkaProducer` object
        """

        broker_host = os.getenv("KAFKA_HOST")
        broker_port = os.getenv("KAFKA_PORT")
        producer = KafkaProducer(
            bootstrap_servers=[f"{broker_host}:{broker_port}"])
        self.logger.info(f"Connected to broker: {broker_host}:{broker_port}")
        return producer

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

        self.producer.send("cowrie", log)

    def close(self) -> None:
        """
        Close the socket connection gracefully
        """

        if self.sock:
            self.sock.close()
            self.sock = None
