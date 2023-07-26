import json
from enum import Enum


class WebhookType(Enum):
    GITLAB = 'GITLAB'
    CONFLUENCE = 'CONFLUENCE'
    JIRA = 'JIRA'
