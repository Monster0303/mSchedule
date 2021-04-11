class Agent:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.hostname = kwargs['hostname']
        self.ip = kwargs['ip']

    def __repr__(self):
        return f"<Agent: {self.id} {self.hostname}>"

    __str__ = __repr__
