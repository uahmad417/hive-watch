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
        self.producer: KafkaProducer = None
        self.sock: socket.socket = None
        self.logger: logging.Logger = self.create_logger()

    def create_logger(self) -> None:
        """
        Setup and configure the logger for this module
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
                    self.process_logs(data.decode("utf-8"), addr)

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

        self.logger.info(f"Log recieved from {addr}: {log}")

    def close(self) -> None:
        """
        Close the socket connection gracefully
        """

        if self.sock:
            self.sock.close()
            self.sock = None
