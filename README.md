Webhook
=========

这是使用`Python`语言`Flask`框架开发的 webhook v3全新版本，支持多种类型的Webhook扩展开发，事件处理机制

#### 快速开始

##### 1. 配置项目webhook

例如,最简单的配置了一个gitlab 类型的webhook , 事件处理类型为通知,以下配置了钉钉机器人

```yaml

config:
  webhooks:
    - webhook_id: finance
      type: GITLAB
      conf:
        gitlab:
          host: http://192.168.10.1:8080/
          private_token: xxxxxxx
      notify:
        ding_talk:
          access_token: "e887b22ce23xxxxxx9a97999xxxxxxee27109dc31c3583bexxx21550c8"
          sign_key: "SEC082117cdxx6be0exxxxxx44c602aa761410bxxxxxxxeb217"


```

##### 启动项目

可在控制台中查看到已经配置好的webhook的地址信息

```text
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.170.83:5000

```

##### 在gitlab后台中填入上面配置好的webhook地址，勾选需要触发的webhook事件。

![](https://img2023.cnblogs.com/blog/994599/202306/994599-20230613112658948-2091790637.png)

##### 配置好与之对应的钉钉群机器人

![](https://img2023.cnblogs.com/blog/994599/202306/994599-20230613113119870-930852617.png)

#### 请求实例:

```text
请求头:X-Gitlab-Event:Push Hook
请求体:
{
  "object_kind": "push",
  "event_name": "push",
  "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
  "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "ref": "refs/heads/master",
  "ref_protected": true,
  "checkout_sha": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "user_id": 4,
  "user_name": "John Smith",
  "user_username": "jsmith",
  "user_email": "john@example.com",
  "user_avatar": "https://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=8://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=80",
  "project_id": 15,
  "project":{
    "id": 15,
    "name":"Diaspora",
    "description":"",
    "web_url":"http://example.com/mike/diaspora",
    "avatar_url":null,
    "git_ssh_url":"git@example.com:mike/diaspora.git",
    "git_http_url":"http://example.com/mike/diaspora.git",
    "namespace":"Mike",
    "visibility_level":0,
    "path_with_namespace":"mike/diaspora",
    "default_branch":"master",
    "homepage":"http://example.com/mike/diaspora",
    "url":"git@example.com:mike/diaspora.git",
    "ssh_url":"git@example.com:mike/diaspora.git",
    "http_url":"http://example.com/mike/diaspora.git"
  },
  "repository":{
    "name": "Diaspora",
    "url": "git@example.com:mike/diaspora.git",
    "description": "",
    "homepage": "http://example.com/mike/diaspora",
    "git_http_url":"http://example.com/mike/diaspora.git",
    "git_ssh_url":"git@example.com:mike/diaspora.git",
    "visibility_level":0
  },
  "commits": [
    {
      "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "message": "Update Catalan translation to e38cb41.\n\nSee https://gitlab.com/gitlab-org/gitlab for more information",
      "title": "Update Catalan translation to e38cb41.",
      "timestamp": "2011-12-12T14:27:31+02:00",
      "url": "http://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "author": {
        "name": "Jordi Mallach",
        "email": "jordi@softcatala.org"
      },
      "added": ["CHANGELOG"],
      "modified": ["app/controller/application.rb"],
      "removed": []
    },
    {
      "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
      "message": "fixed readme",
      "title": "fixed readme",
      "timestamp": "2012-01-03T23:36:29+02:00",
      "url": "http://example.com/mike/diaspora/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
      "author": {
        "name": "GitLab dev user",
        "email": "gitlabdev@dv6700.(none)"
      },
      "added": ["CHANGELOG"],
      "modified": ["app/controller/application.rb"],
      "removed": []
    }
  ],
  "total_commits_count": 4
}



```

#### 通知钉钉群机器人实现效果:

推送事件(Push Hook):

![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5b40cf05991c4e09be7b1a6cc6878bc9~tplv-k3u1fbpfcp-watermark.image?)

议题事件(Issue Hook):

![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/0bd1d11e732e45e7bd99a2e0a5731bdc~tplv-k3u1fbpfcp-watermark.image?)

流水线事件(Pipeline Hook):

![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/be50a07007fe493c83ecb7e0491625bb~tplv-k3u1fbpfcp-watermark.image?)

合并请求事件(Merge Request Hook):

![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/26ecf69c83b14f7ab53b3ecc974230e3~tplv-k3u1fbpfcp-watermark.image?)

目前webhook类型仅实现了Gitlab类型的基本开发,其它类型正在开发中,支持自定义扩展类型

| webhook类型  | 实现类                  | 完成状态 |
|:-----------|:---------------------|:-----|
| GITLAB     | GitlabWebhookHandler | ✔️   |
| JIRA       | 暂无                   | ❌    |
| CONFLUENCE | 暂无                   | ❌    |

目前Gitlab默认支持的事件处理器实现,均支持实现自定义扩展实现
[Gitlab文档地址](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html)

| Gitlab事件类型             | 默认实现类                              | 有默认实现 |
|:-----------------------|:-----------------------------------|:------|
| Push Hook              | PushHookNotifyEventHandler         | ✔️    |
| Pipeline Hook          | PipelineHookNotifyEventHandler     | ️✔️   |
| Merge Request Hook     | MergeRequestHookNotifyEventHandler | ✔️    |
| Tag Push Hook          | TagPushHookNotifyEventHandler      | ✔️    |
| Issue Hook             | IssueHookNotifyEventHandler        | ✔️    |
| Releases Hook          | ReleaseHookNotifyEventHandler      | ✔️    |
| Note Hook              | NoteHookNotifyEventHandler         | ✔️    |
| Job Hook               | JobHookNotifyEventHandler          | ✔️    |
| Confidential Note Hook | 暂无                                 | ❌     |
| Wiki Page Hook         | 暂无                                 | ❌     |
| Deployment Hook        | 暂无                                 | ❌     |
| Feature Flag Hook      | 暂无                                 | ❌     |

目前通知型事件处理类型支持 钉钉机器人,飞书机器人,企业微信机器人,支持自定义扩展通知类型

| 通知类型    | 实现类                | 完成状态 |
|:--------|:-------------------|:-----|
| 钉钉机器人   | DingTalkNotifier   | ✔️   |
| 飞书机器人   | FeiShuNotifier     | ✔️   |
| 企业微信机器人 | CorpWechatNotifier | ❌    |
