import json
from dataclasses import Field
from enum import Enum
from typing import Optional
from pydantic import BaseModel

from meta.webhook_type import WebhookType


class GitLabConf(BaseModel):
    host: Optional[str] = None
    private_token: Optional[str] = None


class WebhookConf(BaseModel):
    gitlab: Optional[GitLabConf] = None


class DingTalkConf(BaseModel):
    access_token: Optional[str] = None
    sign_key: Optional[str] = None
    url: Optional[str] = "https://oapi.dingtalk.com/robot/send"


class FeiShuConf(BaseModel):
    url: Optional[str] = None
    sign_key: Optional[str] = None


class NotifyConf(BaseModel):
    ding_talk: Optional[DingTalkConf] = None
    fei_shu: Optional[FeiShuConf] = None


class Webhook(BaseModel):
    webhook_id: Optional[str] = None
    type: Optional[WebhookType] = None
    conf: Optional[WebhookConf] = None
    notify: Optional[NotifyConf] = None

    def to_dict(self):
        webhook_dict = dict(self)
        for key, value in webhook_dict.items():
            if isinstance(value, Enum):
                # 将枚举类型转换为字符串
                webhook_dict[key] = value.value
            elif isinstance(value, BaseModel):
                webhook_dict[key] = value.model_dump()
        return webhook_dict
