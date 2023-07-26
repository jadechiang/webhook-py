import re
from abc import ABC, abstractmethod

from meta.webhook import Webhook
from notify.notify_message import NotifyMessage


class Notifier(ABC):
    PHONE_PATTERN = re.compile(r"(13\d|14[579]|15[0-3,5-9]|166|17[0135678]|18\d|19[89])\d{8}")

    @abstractmethod
    def process(self, message: NotifyMessage):
        """
        Process the notification message and return the actual request message object.

        :param message: Notification message
        :return: Request message object
        """
        pass

    @abstractmethod
    def notify(self, webhook: Webhook, json_data: dict):
        """
        Notify the message.

        :param webhook: Webhook information
        :param json_data: Request message object
        :return: Result of the notification
        """
        pass
