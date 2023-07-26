from abc import ABC, abstractmethod

from meta.webhook import Webhook

"""
通知消息生成器
"""


class NotifyMessageGenerator(ABC):
    @abstractmethod
    def generate(self, webhook: Webhook, json_data: dict):
        """生成通知消息"""
        pass

    @abstractmethod
    def should_notify(self, webhook: Webhook, json_data: dict):
        """是否执行通知"""
        pass

    @staticmethod
    def get_user_home_page(self, project_url, username):
        """截取消息中的某些字段"""
        return f"{self.get_host_schema(project_url)}/{username}"

    @staticmethod
    def get_host_schema(project_url):
        schema = project_url.split("//")[0]
        body = project_url.split("//")[1]
        host = body.split("/")[0]
        return schema + host
