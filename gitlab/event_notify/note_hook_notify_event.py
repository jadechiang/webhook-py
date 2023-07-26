from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator


class NoteHookNotifyEvent(NotifyMessageGenerator):

    def should_notify(self, _, json_data: dict):
        return True

    def generate(self, _, note_hook):
        message = NotifyMessage()
        message.title = note_hook.get('object_kind', "")
        user = note_hook.get('user', {})
        message.notifies = [str(user.get('id', ""))]

        project = note_hook.get('project', {})
        issue = note_hook.get('issue', {})
        object_attributes = note_hook.get('object_attributes', {})
        sb = []
        u = "[{}]({})".format(user.get('username', ''),
                              super().get_user_home_page(project.get('web_url', ''), user.get('username', '')))
        i = "[#{}]({})".format(issue.get('id', ''), issue.get('url', ''))
        n = "[{}]({})".format(note_hook.get('object_kind', ''), object_attributes.get('url', ''))
        sb.append("<font color='#000000'>{}{} add new {} in Issue{}</font>\n\n".format(u, "🗐", n, i))
        sb.append("**{}**\n\n>{}\n".format(issue.get('title', ''), object_attributes.get('note', '')))

        message.message = "".join(sb)
        return message


note_hook_notify_event = NoteHookNotifyEvent()
