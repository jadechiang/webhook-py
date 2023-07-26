from abc import ABC, abstractmethod
from meta.webhook import Webhook


class WebhookHandler(ABC):

    @abstractmethod
    def handle_webhook(self, webhook: Webhook, json_data: dict):
        """
        处理webhook请求信息
        """
        pass
