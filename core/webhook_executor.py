from core.webhook_handler_factory import webhook_handler_factory
from meta.webhook import Webhook


class WebhookExecutor:
    """
    获取具体的处理器,执行对应的事件
    """

    def handle_webhook(self, webhook: Webhook, json_data: dict):
        webhook_handler = webhook_handler_factory.get_webhook_handler(webhook.type)
        if webhook_handler is None:
            raise NotImplementedError("Unsupported webhook handler")
        return webhook_handler.handle_webhook(webhook, json_data)


webhook_executor = WebhookExecutor()
