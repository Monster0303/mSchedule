import netifaces
import ipaddress
import os
import uuid
import socket


class Message:
    def __init__(self, myidpath):
        # 从文件中读取主机的 UUID
        if os.path.exists(myidpath):
            with open(myidpath) as f:
                self.id = f.readline().strip()  # 配置文件中应该只有一行 uuid 信息
        else:
            self.id = uuid.uuid4().hex
            with open(myidpath, 'w') as f:
                f.write(self.id)

    def _get_addresses(self):
        """ 获取主机上所有接口可用的 IPV4 地址"""
        addresses = []
        for interface in netifaces.interfaces():
            ips = netifaces.ifaddresses(interface)
            if 2 in ips:
                for ip in ips[2]:
                    # ipaddress地址验证
                    # print(ip)
                    ip = ipaddress.ip_address(ip['addr'])

                    # 如果是以下几种，则不要
                    if ip.version != 4:  # 版本
                        continue
                    if ip.is_link_local:  # 169.254 地址
                        continue
                    if ip.is_loopback:  # 回环
                        continue
                    if ip.is_multicast:  # 多播
                        continue
                    if ip.is_reserved:  # 保留
                        continue

                    addresses.append(str(ip))

        return addresses

    def reg(self):
        """生成注册消息"""
        return {
            'type': 'register',
            'payload': {
                'id': self.id,
                'hostname': socket.gethostname(),
                'ip': self._get_addresses()
            }
        }

    def heartbeat(self):
        """生成心跳消息，和 reg 是相似的"""
        return {
            'type': 'heartbeat',
            'payload': {
                'id': self.id,
                'hostname': socket.gethostname(),
                'ip': self._get_addresses()
            }
        }

    def result(self, task_id, code, output):
        """返回任务执行结果的 msg"""
        return {
            'type': 'result',
            'payload': {
                'id': task_id,
                'agent_id': self.id,
                'code': code,
                'output': output
            }
        }
