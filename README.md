# 任务调度系统
类似于 ansible 功能，分发脚本到目标节点上去执行，更加简单，满足企业需求。

采用的 CS 的设计编程模式，分为 Master、 Agent。

**架构图**：
![image](https://user-images.githubusercontent.com/40815364/114294282-191ae480-9ad0-11eb-9bbb-79742d41ed83.jpeg)
 
# Master 设计
- 使用模块：aiohttp 和 zerorpc
1. TCP Server：绑定端口，启动监听，等待 Agent 连接。
2. 信息存储：存储 Agent 列表
3. 存储用户提交的 Task 列表：将用户通过 WEB 提交的任务信息存储下来。
4. 接收注册：将注册信息写入 Agent 列表
5. 接收心跳信息：接收 Agent 发来的心跳信息
6. 派发任务：将用户提交的任务分配到 Agent 端

# Agent 设计
1. 注册信息：Agent 启动后，需要主动联系 Server，注册自己的信息。
2. 心跳信息：Agent 定时向 Master 发送心跳包，包含 UUID，附带 hostname 和 ip
3. 任务消息：Master 分派任务给 Agent。
4. 任务结果消息：当 Agent 执行完任务，返回给 Master 该任务的状态码和输出结果。
