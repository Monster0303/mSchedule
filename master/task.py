import uuid
from .state import *


class Task:
    def __init__(self, task_id, script, targets, timeout=0, parallel=1, fail_rate=0, fail_count=-1):
        self.id = task_id
        # ↓ 整个任务的运行状态
        self.state = WAITING
        self.script = script
        self.timeout = timeout
        # ↓ 用来执行的 agent 节点，记录 agent 上的 state 和输出 output
        self.targets = {agent_id: {'state': WAITING, 'output': ""} for agent_id in targets}  # TODO 为了使用方便以后可以加分组
        self.target_count = len(self.targets)
        self.parallel = parallel  # 并行率，未实现
        self.fail_rate = fail_rate  # 失败率，未实现
        self.fail_count = fail_count  # 失败次数，未实现
