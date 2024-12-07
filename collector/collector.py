import os
import socket
import logging

if __name__ == "__main__":

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

    host = os.environ.get("SYSLOG_HOST")
    port = int(os.environ.get("SYSLOG_PORT"))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()

        logger.info(f"Listening for messages on {host}:{port}...")

        while True:
            conn, addr = sock.accept()
            with conn:
                logger.info(f"Connected by {addr}")

                data = conn.recv(4096)

                if not data:
                    break
                logger.info(f"Recieved message from {addr}: {data.decode('utf-8')}")
