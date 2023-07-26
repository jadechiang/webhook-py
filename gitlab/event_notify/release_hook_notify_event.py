from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator


class ReleaseHookNotifyEvent(NotifyMessageGenerator):
    def should_notify(self, _, json_data: dict):
        return "update" != json_data.get('action', "")

    def generate(self, _, release_hook):
        message = NotifyMessage()
        message.title = release_hook.get("object_kind")
        message.notifies = None
        tag = release_hook.get("tag")
        project = release_hook.get("project")
        assets = release_hook.get("assets")

        tags = f"[{tag}]({project.get('web_url')}/-/tags/{tag})"
        head = f"<font color='#000000'>[{project.get('name')}]({project.get('web_url')}) {release_hook.get('action')}" \
               f" new {release_hook.get('object_kind')} [{release_hook.get('name')}]({release_hook.get('url')}) 📌{tags} 🚀🚀🚀\n"
        context = head

        for source in assets.get("sources"):
            context += f"> - [📁 Source code ({source.get('format')})]({source.get('url')})\n"

        message.message = context
        return message


release_hook_notify_event = ReleaseHookNotifyEvent()
