from collector import Collector, test

if __name__ == "__main__":
    col = Collector()
    col.start()
    col.recieve_logs()
