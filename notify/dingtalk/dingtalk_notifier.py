import time
import hmac
import hashlib
import base64
from urllib.parse import quote

import requests

from meta.webhook import Webhook
from notify.notifier import Notifier
from notify.notify_message import NotifyMessage


class DingTalkNotifier(Notifier):

    def process(self, message: NotifyMessage):
        # todo 这样直接构建不好后期应该换成对象
        send_message = {
            "msgtype": "markdown"
        }
        markdown = {
            "title": message.title
        }
        sb = []
        if message.notifies:
            notifies = message.notifies
            at_mobiles = []
            for notifier in notifies:
                if notifier and super().PHONE_PATTERN.match(notifier):
                    sb.append(f"@{notifier}")
                    at_mobiles.append(notifier)
            if sb:
                sb.append("\n\n")
            send_message["at"] = {"atMobiles": at_mobiles,
                                  "atUserIds": None,
                                  "isAtAll": False,
                                  "atMobilesString": None
                                  }

        sb.append(message.message)
        markdown["text"] = "\n".join(sb)
        send_message["markdown"] = markdown
        return send_message

    def notify(self, webhook: Webhook, json_data: dict):
        dingtalk = webhook.notify.ding_talk
        headers = {'Content-Type': 'application/json'}
        timestamp = int(time.time() * 1000)
        sign = self.sign(timestamp, dingtalk.sign_key)
        url = f"https://oapi.dingtalk.com/robot/send?access_token={dingtalk.access_token}&timestamp={timestamp}&sign={sign}"
        response = requests.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def sign(timestamp: int, secret: str) -> str:
        string_to_sign = f"{timestamp}\n{secret}"
        hmac_digest = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        signature_data = base64.b64encode(hmac_digest).decode('utf-8')
        return quote(signature_data, safe='')
