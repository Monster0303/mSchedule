import datetime
from .task import Task
from .state import *
import uuid


class Storage:
    def __init__(self):
        self.agents = {}
        # agents = {'agent_id':
        #               {'timestamp': 1607315039.053493,  # 最后发送心跳的时间
        #                'busy': False,  # 是否繁忙，暂未实现
        #                'info': {'id': '3d947e4d9de443e3b8c0e0a7459c124d',  # agent 其他信息
        #                         'hostname': 'MacBookPro',
        #                         'ip': ['192.168.50.30', '10.211.55.2', '10.37.129.2']
        #                         }
        #                }
        #           }
        self.tasks = {}
        # tasks: {task_id: task实例}

    def reg_hb(self, **payload):
        agent_id = payload['id']
        agent = self.agents.get(agent_id)
        if not agent:
            agent = {}

        agent['timestamp'] = datetime.datetime.now().timestamp()
        agent['busy'] = False
        agent['info'] = payload
        self.agents[agent_id] = agent

    def get_agents(self):
        return list(self.agents.keys())

    def add_task(self, msg: dict):
        msg['task_id'] = uuid.uuid4().hex
        task = Task(**msg)
        self.tasks[task.id] = task
        return task.id

    def iter_tasks(self, states=(WAITING, RUNNING)):
        # 把不符合条件的 task 过滤掉，为了加快迭代速度
        yield from (task for task in self.tasks.values() if task.state in states)

    def get_task(self, agent_id):
        """agent 拉取任务"""
        for task in self.iter_tasks():  # 迭代过滤后的任务列表
            if agent_id in task.targets:  # 如果此 agent 在 task 的 targets 中，就。。。
                if task.state == WAITING:
                    task.state = RUNNING
                task.targets[agent_id]['state'] = RUNNING
                print([(task.id, task.state, task.script) for task in self.tasks.values()])
                return [task.id, task.script, task.timeout]

    def result(self, msg: dict):  # msg: 'id': task_id, 'agent_id': self.id, 'code': code, 'output': output
        task = self.tasks[msg['id']]
        agent = task.targets[msg['agent_id']]

        # 判断当前 agent 运行结果
        if msg['code'] == 0:
            agent['state'] = SUCCEED
        else:
            agent['state'] = FAILED

        # 判断当前任务运行结果，有一条失败即为失败  TODO 如果未来要按照任务总数的百分比判断，则需要更多的判断条件
        for agent in task.targets.values():
            task.state = SUCCEED if agent['state'] == SUCCEED else FAILED

        print([(task.id, task.state, task.script) for task in self.tasks.values()])
