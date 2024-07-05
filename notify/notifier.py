import re
from abc import ABC, abstractmethod

from meta.webhook import Webhook
from notify.notify_message import NotifyMessage


class Notifier(ABC):
    PHONE_PATTERN = re.compile(r"(13\d|14[579]|15[0-3,5-9]|166|17[0135678]|18\d|19[89])\d{8}")

    @abstractmethod
    def process(self, message: NotifyMessage):
        """
        处理通知消息并返回实际的请求消息对象。.
        :param message: 通知消息
        :return: 请求消息对象
        """
        pass

    @abstractmethod
    def notify(self, webhook: Webhook, json_data: dict):
        """
        通知消息。
        :param webhook: Webhook信息
        :param json_data: 请求消息对象
        :return:通知结果
        """
        pass
