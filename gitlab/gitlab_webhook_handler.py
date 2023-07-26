from core.webhook_handler import WebhookHandler
from gitlab.event_notify import handlers
from gitlab.gitlab_event_factory import gitlab_event_factory
from meta.webhook import Webhook
from flask import g

from notify.notifier_factory import notifier_factory


class GitlabWebhookHandler(WebhookHandler):

    def handle_webhook(self, webhook: Webhook, json_data: dict):
        # 从 g 对象中获取请求对象
        local_request = g.request
        gitlab_event = local_request.headers.get('X-Gitlab-Event')
        if not gitlab_event:
            raise NotImplementedError(
                "Unable to get the Gitlab event type, please check that your webhook configuration is correct")
        # 针对某一事件可能有多个事件处理器 TODO:没测试过多个的情况可以能需要修改
        event_handlers = gitlab_event_factory.get_event_handlers(gitlab_event, webhook)
        resp = []
        for handler in event_handlers:
            # What event is the process
            notify_event = handlers.get(handler)
            if notify_event is not None and notify_event.should_notify(webhook, json_data):
                # 生成通知消息
                message = notify_event.generate(webhook, json_data)
                # 有哪些平台需要通知
                notifiers = notifier_factory.get_notifies(webhook)
                for notifier in notifiers:
                    response_json = notifier.notify(webhook, notifier.process(message))
                    resp.append(response_json)

        # 通知
        return resp[0] if len(resp) == 1 else resp
