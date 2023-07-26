from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator


class PushHookNotifyEvent(NotifyMessageGenerator):
    """是否执行通知看看必填的参数有没有填"""

    def should_notify(self, _, json_data: dict):
        return bool(json_data.get('commits'))

    def generate(self, _, push_hook):
        message = NotifyMessage()
        message.title = push_hook.get("object_kind", "")
        message.notifies = [str(push_hook.get("user_id", ""))]
        commits = push_hook.get("commits", [])
        project = push_hook.get("project", {})
        user_username = push_hook.get("user_username")
        commits.sort(key=lambda x: x.get("id", ""))
        sb = []
        ref = push_hook.get("ref", "")
        branch = ref.replace("refs/heads/", "")
        sb.append(f"[[{project.get('name', '')}:{branch}]]({project.get('web_url', '')}/-/tree/{branch})")

        c = "commits" if len(commits) > 1 else "commit"
        user = push_hook.get("user_name") if \
            user_username is None else "[{}]({})" \
            .format(user_username, super().get_user_home_page(self, project.get("web_url", ""), user_username))
        sb.append("<font color='#000000'>{} {} new {}"
                  " by {} {} </font>\n\n".format(push_hook.get("event_name", ""),
                                                 push_hook.get("total_commits_count", ""), c, "\U0001F600",
                                                 user))
        for commit in commits:
            sb.append("> [{}]({}) {} - {}\n\n".format(commit.get("id", "")[:8], commit.get("url", ""),
                                                      commit.get("author", {}).get("name", ""),
                                                      commit.get("title", "")))
        message.message = "".join(sb)
        return message


push_hook_notify_event = PushHookNotifyEvent()
