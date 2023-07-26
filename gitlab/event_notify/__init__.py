from gitlab.event_notify.issue_hook_notify_event import issue_hook_notify_event
from gitlab.event_notify.job_hook_notify_event import job_hook_notify_event
from gitlab.event_notify.merge_request_hook_notify_event import merge_request_hook_notify_event
from gitlab.event_notify.note_hook_notify_event import note_hook_notify_event
from gitlab.event_notify.pipeline_hook_notify_event import pipeline_hook_notify_event
from gitlab.event_notify.push_hook_notify_event import push_hook_notify_event
from gitlab.event_notify.release_hook_notify_event import release_hook_notify_event
from gitlab.event_notify.tag_push_hook_notify_event import tag_push_hook_notify_event

"""
具体文档地址:https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html
"""
handlers = {
    "push_hook_notify_event": push_hook_notify_event,
    "issue_hook_notify_event": issue_hook_notify_event,
    "job_hook_notify_event": job_hook_notify_event,
    "merge_request_hook_notify_event": merge_request_hook_notify_event,
    "pipeline_hook_notify_event": pipeline_hook_notify_event,
    "tag_push_hook_notify_event": tag_push_hook_notify_event,
    "note_hook_notify_event": note_hook_notify_event,
    "release_hook_notify_event": release_hook_notify_event
}
