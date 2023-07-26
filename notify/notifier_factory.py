from typing import List, Type, Dict
from collections import defaultdict

from meta.webhook import Webhook
from notify.dingtalk.dingtalk_notifier import DingTalkNotifier
from notify.feishu.feishu_notifier import FeiShuNotifier
from notify.notifier import Notifier


class WebhookNotifierFactory:

    def get_notifies(self, webhook: Webhook) -> List['Notifier']:
        notifiers = []
        if not notifiers:
            if webhook.notify.ding_talk is not None:
                notifiers.append(self.get_notifier(DingTalkNotifier))
            if webhook.notify.fei_shu is not None:
                notifiers.append(self.get_notifier(FeiShuNotifier))
        return notifiers

    @staticmethod
    def get_notifier(notifier_class: Type['Notifier']) -> 'Notifier':
        return notifier_class()


notifier_factory = WebhookNotifierFactory()
