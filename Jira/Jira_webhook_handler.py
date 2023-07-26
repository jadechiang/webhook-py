from core.webhook_handler import WebhookHandler
from meta.webhook import Webhook


class JiraWebhookHandler(WebhookHandler):

    def handle_webhook(self, webhook: Webhook, json_data: dict):
        return '暂未开发,屯其膏，小贞吉，大贞凶。'
