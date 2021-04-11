from aiohttp import web
import zerorpc

client = zerorpc.Client()
client.connect('tcp://127.0.0.1:9000')


async def targets_handler(request: web.Request):
    txt = client.get_agents()
    return web.json_response(txt)


async def add_task_handler(request: web.Request):
    data = await request.json()
    return web.json_response(client.add_task(data), status=201)


app = web.Application()
app.router.add_get('/task/agents', targets_handler)
app.router.add_post('/task', add_task_handler)

web.run_app(app, host='0.0.0.0', port=9000)

# postman 中的测试数据
GET = {'url': '192.168.50.30:9000/task/agents'}
POST = {'url': '192.168.50.30:9000/task',
        'body_json': {
            "script": "echo 'hello'",
            "timeout": 30,
            "targets": ["3d947e4d9de443e3b8c0e0a7459c124d"]}
        }
