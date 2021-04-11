import zerorpc
import threading
from .msg import Message
from .config import INTERVAL
from utils import getlogger
from .executor import Executor
from .state import *

logger = getlogger(__name__, f'/tmp/{__name__}.log')


class ConnectionManager:
    def __init__(self, master_url, message: Message):
        self.master_url = master_url
        self.message = message  # 对象
        self.client = zerorpc.Client()
        self.event = threading.Event()
        self.state = WAITING  # 任务完成的状态
        self.exec = Executor()

    def start(self):
        try:
            self.event.clear()  # 重置event
            print('已重置')
            # 连接
            self.client.connect(self.master_url)
            print('已连接')
            # 注册
            self._send(self.message.reg())
            # 心跳循环
            print('heart')
            while not self.event.wait(INTERVAL):
                self._send(self.message.heartbeat())    # 心跳

                if self.state == WAITING:
                    task = self.client.get_task(self.message.id)    # Message 的实例
                    if task:
                        # task --- [task.id, task.script, task.timeout]
                        code, output = self.exec.run(task[1], task[2])  # 阻塞    TODO 单开线程，异步架构
                        self._send(self.message.result(task[0], code, output))
                        self.state = WAITING
                        logger.info(f'state: {code}, output:{output}')

        except Exception as e:
            logger.error(f'Failed to connect to master. Error: {e}')
            raise e

    def _send(self, msg):
        ack = self.client.sendmsg(msg)
        logger.info(ack)

    def shutdown(self):
        self.event.set()
        # self.client.close()   # 打开这个，客户端就无法重连了
