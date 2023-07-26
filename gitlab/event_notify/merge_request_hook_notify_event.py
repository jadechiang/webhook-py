from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator


class MergeRequestHookNotifyEvent(NotifyMessageGenerator):

    def should_notify(self, _, json_data: dict):
        return "update" != json_data.get('object_attributes', {}).get('action', '')

    def generate(self, _, merge_request_hook):
        message = NotifyMessage()
        message.title = merge_request_hook.get('object_kind', "")
        message.notifies = [str(merge_request_hook['user'].get('id', ""))]

        user = merge_request_hook['user']
        project = merge_request_hook['project']
        object_attributes = merge_request_hook['object_attributes']
        sb = []
        p = "[[{}]]({})".format(project.get('name', ''), project.get('web_url', ''))
        sources = "[{}]({}/-/tree/{})".format(object_attributes.get('source_branch', ''), project.get('web_url', ''),
                                              object_attributes.get('source_branch', ''))
        targets = "[{}]({}/-/tree/{})".format(object_attributes.get('target_branch', ''), project.get('web_url', ''),
                                              object_attributes.get('target_branch', ''))
        u = "[{}]({})".format(user.get('username', ''),
                              super().get_user_home_page(project.get('web_url', ''), user.get('username', '')))
        merge = " [{}]({})({})".format(object_attributes.get('id', ''), object_attributes.get('url', ''),
                                       object_attributes.get('title', ''))
        sb.append("<font color='#000000'>{} {} {} {} {}</font>\n\n".format(p, u, object_attributes.get('state', ''),
                                                                           merge_request_hook.get('object_kind', ''),
                                                                           merge))
        if object_attributes.get('state', '') == "opened":
            sb.append(" \uD83D\uDE00 {} wants to merge {} ➔➔ {}\n".format(user.get('username', ''), sources, targets))
            c = " {} - {}\n".format(object_attributes.get('last_commit', {}).get('author', {}).get('name', ''),
                                    object_attributes.get('last_commit', {}).get('message', ''))
            sb.append(">[{}]({}){}".format(object_attributes.get('last_commit', {}).get('id', '')[:8],
                                           object_attributes.get('last_commit', {}).get('url', ''), c))
        elif object_attributes.get('state', '') == "merged":
            sb.append(" \uD83D\uDE00 {} has completed the merge {}➔➔{}✔️\n".format(user.get('username', ''), sources,
                                                                                   targets))
        elif object_attributes.get('state', '') == "closed":
            sb.append(
                " \uD83D\uDE36 {} has closed the merge {}➔➔{}🚫\n".format(user.get('username', ''), sources, targets))

        message.message = "".join(sb)
        return message


merge_request_hook_notify_event = MergeRequestHookNotifyEvent()
