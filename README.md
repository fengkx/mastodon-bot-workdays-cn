# 今年还有几天班要上
一个每天提醒你今年有几天班要上（中国大陆地区法定假期），还剩几天假的<a rel="me" href="https://mastodon.online/@working_days_cn">Mastodon</a>机器人

## Development

使用 [pdm](https://github.com/pdm-project/pdm) 来管理 virtualenv 和 dependencies。可以考虑使用[pipx](https://pypa.github.io/pipx/) 安装pdm

```sh
pdm install -G:all #安装依赖
make lint #静态检查
make test #执行测试
```

