from flask import request, jsonify, g

from core import app, webhook_repository
from core.webhook_executor import webhook_executor

ENDPOINT_URL = "/actuator"


@app.route(ENDPOINT_URL + "/<webhook_id>", methods=['POST'])
def webhook(webhook_id):
    app.logger.info(f'Request received: {request.method} {request.url}')
    # 存储请求上下文到 Flask 的 g 对象中
    g.request = request
    # 获取请求的JSON数据
    json_data = request.get_json()
    print(json_data)
    # 根据 id 查询 webhook
    web_hook = webhook_repository.find_by_id(webhook_id)

    if web_hook is None:
        return jsonify({"message": "Webhook not found"}), 404

    response = webhook_executor.handle_webhook(web_hook, json_data)
    return jsonify(response), 200
