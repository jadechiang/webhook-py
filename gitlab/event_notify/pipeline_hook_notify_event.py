from notify.notify_message import NotifyMessage
from notify.notify_message_generator import NotifyMessageGenerator
import datetime


class PipelineHookNotifyEvent(NotifyMessageGenerator):

    def should_notify(self, _, json_data: dict):
        return "pending" != json_data.get('object_attributes', {}).get('status', '')

    def generate(self, _, pipeline_hook):
        message = NotifyMessage()
        message.title = pipeline_hook.get('object_kind', "")
        message.notifies = [str(pipeline_hook['user'].get('id', ""))]

        sb = []
        object_attributes = pipeline_hook['object_attributes']
        project = pipeline_hook['project']
        commit = pipeline_hook['commit']
        builds = pipeline_hook['builds']
        status = object_attributes.get('status', "")

        pipeline = f"{pipeline_hook.get('object_kind', '')} [#{object_attributes.get('id', '')} 🚀]" \
                   f"({project.get('web_url', '')}/-/pipelines/{object_attributes.get('id', '')})"
        sb.append(
            f"[[{project.get('name', '')}:{object_attributes.get('ref', '')}]]({project.get('web_url', '')}"
            f"/-/tree/{object_attributes.get('ref', '')}) <font color='#000000'>{pipeline} {status}</font>\n\n")

        if status != "running":
            total_time = (object_attributes.get('duration', 0) or 0) + (object_attributes.get('queuedDuration', 0) or 0)
            formatted_time = str(datetime.timedelta(seconds=total_time))

            sb.append(
                f">{commit.get('id', '')[:8]} [{commit.get('url', '')}]({commit.get('author', {}).get('name', '')}) -"
                f" {commit.get('title', '')}\n\n")

            status_emoji, status_color = get_status_emoji_and_color(status)
            sb.append(
                f"{status_emoji}{pipeline} : <font color='{status_color}'>{object_attributes.get('detailedStatus', '')} "
                f"🗗 {formatted_time}</font>\n\n")

            sorted_builds = sorted(builds, key=lambda x: x.get('duration', 0) or 0, reverse=True)

            for build in sorted_builds:
                cost_time = str(datetime.timedelta(seconds=build.get('duration', 0) or 0))

                color, emoji = get_status_emoji_and_color(build.get('status', ''))

                file_name = build.get('artifactFile', {}).get('filename', '')
                file_size = build.get('artifactFile', {}).get('size', 0)
                formatted_file_size = get_formatted_file_size(file_size)
                file_link = f"[{file_name}]({project.get('web_url', '')}/-/jobs/{build.get('id', '')}/artifacts/download)"

                sb.append(
                    f">{emoji} {build.get('stage', '')} [{project.get('web_url', '')}]({build.get('id', '')}) : <font color='{color}'>{build.get('status', '')} {file_link} {formatted_file_size} 🗗 {cost_time}</font>\n\n")
        else:
            pipeline_endpoint_url = "gitlab/pipeline"
            # todo ip地址不能写死要拿到环境
            localhost_ip = "localhost"
            port = 80
            host_schema = f"http://{localhost_ip}:{port}/{pipeline_endpoint_url}"
            sb.append(
                f"[🚫取消运行]({host_schema}/cancel?projectId={project.get('id', '')}&pipelineId={object_attributes.get('id', '')}) ")
            sb.append(
                f"[♻️重新运行]({host_schema}/retry?projectId={project.get('id', '')}&pipelineId={object_attributes.get('id', '')}) ")
            sb.append(
                f"[⛔删除]({host_schema}/delete?projectId={project.get('id', '')}&pipelineId={object_attributes.get('id', '')})\n\n")

        message.message = "".join(sb)
        return message


"""根据文件长度得到文件大小(比如 : 1.81GB,1.83MB)"""


def get_formatted_file_size(size):
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size >= 1024 and i < len(size_name) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {size_name[i]}"


def get_status_emoji_and_color(status):
    status_emoji = ""
    status_color = ""
    if status == "success":
        status_emoji = "✅"
        status_color = "#00b140"
    elif status == "failed":
        status_emoji = "❌"
        status_color = "#ff0000"
    elif status == "canceled":
        status_emoji = "⏹️"
        status_color = "#FFDAC8"
    elif status == "skipped":
        status_emoji = "⏭️"
        status_color = "#8E8E8E"
    elif status == "manual":
        status_emoji = "\uD83D\uDD04"
        status_color = "#8E8E8E"
    return status_emoji, status_color


pipeline_hook_notify_event = PipelineHookNotifyEvent()
