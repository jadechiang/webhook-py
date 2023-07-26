from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator


class JobHookNotifyEvent(NotifyMessageGenerator):

    def should_notify(self, _, json_data: dict):
        return True

    def generate(self, _, job_hook):
        message = NotifyMessage()
        message.title = job_hook.get('object_kind', "")
        message.notifies = [str(job_hook['user'].get('id', ""))]
        repository = job_hook.get('repository', {})
        pipeline_id = job_hook.get('pipeline_id', 0)
        build_status = job_hook.get('build_status', "")
        project = f"[[{repository.get('name', '')}]]({repository.get('homepage', '')})"
        pipeline = f"pipeline[# {pipeline_id}]({repository.get('homepage', '')}/-/pipelines/{pipeline_id})"
        cost_time = f"{job_hook.get('build_duration', 0.0):.0f}"
        if not cost_time:
            cost_time = "0"
        emoji = ""
        color = "#000000"
        if build_status == "success":
            color = "#00b140"
            emoji = "✔️"
        elif build_status == "failed":
            color = "#ff0000"
            emoji = "❌"
        elif build_status == "canceled":
            color = "#FFDAC8"
            emoji = "⏹️"
        elif build_status == "skipped":
            color = "#8E8E8E"
            emoji = "⏭️"
        build = f"<font color='{color}'> [{job_hook.get('build_stage', '')}]({repository.get('homepage', '')}/-/jobs/{job_hook.get('build_id', None)}) {build_status} {emoji}</font>"
        message.message = f"<font color='#000000'>{project} {pipeline} {build} \uD83D\uDD57 {cost_time}s</font>"
        return message


job_hook_notify_event = JobHookNotifyEvent()
