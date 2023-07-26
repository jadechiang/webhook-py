import hashlib
import hmac
import base64
import time
from urllib.parse import quote

import requests

from meta.webhook import Webhook
from notify.notifier import Notifier
from notify.notify_message import NotifyMessage


class FeiShuNotifier(Notifier):
    def process(self, message: NotifyMessage):
        # todo 这样直接构建不好后期应该换成对象
        send_message = {
            "msg_type": "interactive"
        }
        card = {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            }
        }
        header = {
            "title": {
                "content": message.title,
                "tag": "plain_text"
            }
        }
        card["header"] = header
        elements = [
            {
                "tag": "markdown",
                "content": message.message,
                "href": None
            }
        ]
        card["elements"] = elements
        send_message["card"] = card
        return send_message

    def notify(self, webhook: Webhook, interactive_message: dict):
        fei_shu = webhook.notify.fei_shu
        sign_key = fei_shu.sign_key
        if sign_key and sign_key.strip():
            timestamp = int(time.time() * 1000)
            sign = self.sign(timestamp, sign_key)
            interactive_message.timestamp = str(timestamp)
            interactive_message.sign = sign
        headers = {"Content-Type": "application/json"}
        response = requests.post(fei_shu.get("url"), json=interactive_message, headers=headers)
        return response.json()

    @staticmethod
    def sign(timestamp: int, sign_key: str) -> str:
        string_to_sign = f"{timestamp}\n{sign_key}"
        hmac_digest = hmac.new(sign_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        signature_data = base64.b64encode(hmac_digest).decode('utf-8')
        return quote(signature_data, safe='')
