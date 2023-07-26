from meta.webhook import Webhook
import re


class GitlabEventFactory:
    @staticmethod
    def get_event_handlers(gitlab_event: str, webhook: Webhook):
        event_handlers = []
        if webhook.notify:
            bean_name = re.sub(r'\s+', '_', gitlab_event.lower()) + '_notify_event'
            event_handlers.append(bean_name)
            return event_handlers


gitlab_event_factory = GitlabEventFactory()
