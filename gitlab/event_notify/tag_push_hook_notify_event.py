from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator


class TagPushHookNotifyEvent(NotifyMessageGenerator):

    def should_notify(self, _, json_data: dict):
        return 'tag_push' == json_data.get('object_kind', '')

    def generate(self, _, tag_push_hook):
        message = NotifyMessage()
        message.title = tag_push_hook.get('object_kind', "")
        message.notifies = [str(tag_push_hook.get('user_id', ""))]

        project = tag_push_hook['project']
        user_username = tag_push_hook.get('user_username', "")
        ref_split = tag_push_hook.get('ref', "").split("/")
        tag = ref_split[-1]
        t = f"[{tag}]({project.get('web_url', '')}/-/tree/{tag})"
        p = f"[{project.get('name', '')}]({project.get('web_url', '')})"
        user = f"[{user_username}]({super().get_user_home_page(project.get('web_url', ''), user_username)})"
        emoji = "\uD83D\uDE80" * 3  # 重复3次 🚀 表情
        message.message = f"{p} push new tag({t}) by {user} {emoji}\n\n > {tag_push_hook.get('message', '')}"
        return message


tag_push_hook_notify_event = TagPushHookNotifyEvent()
