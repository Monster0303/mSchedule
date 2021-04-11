from .storage import Storage
from utils import getlogger

# agent[msg['payload']['id']] = msg['payload']['hostname'], msg.get('payload').get('ip')

logger = getlogger(__name__, f'/tmp/{__name__}.log')


class ConnectionManager:
    def __init__(self):
        self.store = Storage()

    def sendmsg(self, msg):  # RPC 对外的接口，其中处理客户端传来的数据
        try:
            if msg['type'] in {'register', 'heartbeat'}:
                self.store.reg_hb(**msg['payload'])
            elif msg['type'] == 'result':
                self.store.result(msg['payload'])
            logger.info(msg)
            return f"ACK: {msg}"
        except Exception as e:
            logger.error(e)
            return 'Bas Request'

    def add_task(self, msg: dict):
        return self.store.add_task(msg)

    def get_task(self, agent_id):
        return self.store.get_task(agent_id)

    def get_agents(self):
        return self.store.get_agents()
