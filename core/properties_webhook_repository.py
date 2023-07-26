from core.webhook_repository import WebhookRepository


class PropertiesWebhookRepository(WebhookRepository):
    def __init__(self, properties):
        super().__init__()
        self.properties = properties
        self.webhooks = {webhook.webhook_id: webhook for webhook in properties.webhooks}

    def get_webhooks(self):
        return self.webhooks

    def find_by_id(self, webhook_id):
        return self.webhooks.get(webhook_id)

    def remove(self, webhook_id):
        if webhook_id in self.webhooks:
            self.webhooks.pop(webhook_id)
