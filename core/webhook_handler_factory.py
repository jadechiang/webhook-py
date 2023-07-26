from core import webhook_handlers
from meta.webhook_type import WebhookType


class WebhookHandlerFactory:
    """
    装饰器
    当类被定义时，它会立即被注册到 WebhookHandlerFactory 实例的 webhook_handlers 字典中。装饰器的作用是在类定义期间自动完成注册的过程。
    """

    @staticmethod
    def register_webhook_handler(webhook_type: WebhookType):
        def decorator(clz):
            webhook_handlers[webhook_type] = clz()
            return clz

        return decorator

    @staticmethod
    def get_webhook_handler(webhook_type: WebhookType):
        return webhook_handlers.get(webhook_type)


webhook_handler_factory = WebhookHandlerFactory()
