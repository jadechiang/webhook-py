import os
import yaml
from typing import List
from pydantic import BaseModel, Field
from pydantic.v1 import root_validator
from meta.webhook import Webhook


class WebhookProperties(BaseModel):
    webhooks: List[Webhook] = Field(..., min_items=1)

    @root_validator
    def validate_webhooks(self, webhook):
        if not webhook:
            raise ValueError("请配置webhooks")
        return webhook


config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'config.yaml')).replace(
    '\\',
    '/')
# 加载YAML配置文件
with open(config_file_path) as file:
    config = yaml.safe_load(file)
