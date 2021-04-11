import zerorpc
from .config import MASTER_URL
from .cm import ConnectionManager


class Master:
    def __init__(self):
        self.server = zerorpc.Server(ConnectionManager())

    def start(self):
        self.server.bind(MASTER_URL)
        self.server.run()

    def shutdown(self):
        self.server.close()
