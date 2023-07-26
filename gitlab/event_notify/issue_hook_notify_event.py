from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator


class IssueHookNotifyEvent(NotifyMessageGenerator):
    """是否执行通知看看必填的参数有没有填"""

    def should_notify(self, _, json_data: dict):
        return "update" != json_data.get('object_attributes', {}).get('action', '')

    def generate(self, _, issue_hook):
        message = NotifyMessage()
        message.title = issue_hook.get('object_kind', "")
        user = issue_hook.get('user', {})
        message.notifies = [str(user.get('id', ""))]
        object_attributes = issue_hook.get('object_attributes', {})
        project = issue_hook.get('project', {})
        sb = []
        project_url = "[{}]({})".format(project.get('name', ""), project.get('web_url', ""))
        issue = "[#{}]({})".format(object_attributes.get('id', ""), object_attributes.get('url', ""))
        title_emoji = ""
        status_emoji = ""
        if object_attributes.get('state', "") == "opened":
            title_emoji = "\uD83D\uDD34"
            status_emoji = "\uD83D\uDE4B\u200D♂️"
        elif object_attributes.get('state', "") == "closed":
            title_emoji = "\uD83D\uDFE2"
            status_emoji = "✌️"
        sb.append("#### {}{} **{}**\n".format(title_emoji, project_url, object_attributes.get('title', "")))
        sb.append("<font color='#000000'>The Issue {} {}{} by [{}]({})</font>\n>{}".format(issue, object_attributes.get(
            'state', ""), status_emoji, user.get('username', ""), super().get_user_home_page(project.get('web_url', ""),
                                                                                             user.get('username', "")),
                                                                                           object_attributes.get(
                                                                                               'description', "")))
        message.message = "".join(sb)
        return message


issue_hook_notify_event = IssueHookNotifyEvent()
