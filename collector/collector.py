import os
import socket

if __name__ == "__main__":

    host = os.environ.get("SYSLOG_HOST")
    port = os.environ.get("SYSLOG_PORT")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()

        print(f"Listening for messages on {host}:{port}...")

        while True:
            conn, addr = sock.accept()
            with conn:
                print(f"Connected by {addr}")

                data = conn.recv(4096)

                if not data:
                    break
                print(f"Recieved message from {addr}: {data.decode('utf-8')}")
