from flask import Flask
from Jira.Jira_webhook_handler import JiraWebhookHandler
from core.properties_webhook_repository import PropertiesWebhookRepository
from core.webhook_properties import WebhookProperties, config
from gitlab.gitlab_webhook_handler import GitlabWebhookHandler
from meta.webhook_type import WebhookType

# 启动设置
app = Flask(__name__)
app.debug = False


# 日志打印
def print_open_endpoints():
    # 获取应用中所有注册的路由信息并记录日志
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                print(
                    f"IP Address: {app.config['HOST_IP']}, Port: {app.config['HOST_PORT']}, "
                    f"Endpoint: {rule.endpoint}, Method: {','.join(rule.methods)}, Path: {rule.rule}")


# 哪些Handler
webhook_handlers = {
    WebhookType.GITLAB: GitlabWebhookHandler(),
    WebhookType.JIRA: JiraWebhookHandler()
}

# 启动加载数据
properties = WebhookProperties.model_validate(config.get('config', {}))
webhook_repository = PropertiesWebhookRepository(properties)
