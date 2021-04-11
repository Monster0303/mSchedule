from .cm import ConnectionManager
from .msg import Message
from .config import MASTER_URL, MYID_PATH
import threading


class Agent:
    # 管理连接，开启连接，负责重连，关闭连接。

    def __init__(self):
        self.msg = Message(MYID_PATH)
        self.cm = ConnectionManager(MASTER_URL, self.msg)
        self.event = threading.Event()

    def start(self):
        # 负责重连
        while not self.event.is_set():
            print('reset')
            try:
                self.cm.start()  # 正常时会阻塞在这
            except:
                print('error !!!!')
                self.cm.shutdown()

            self.event.wait(3)

    def shutdown(self):
        self.event.set()
        self.cm.shutdown()
