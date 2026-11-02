# 今年还有几天班要上
一个每天提醒你今年有几天班要上(中国大陆地区法定假期)，还剩几天假的 <a rel="me" href="https://mastodon.online/@working_days_cn">Mastodon</a> 机器人

## Development

GitHub Actions 使用 `ubuntu-latest`，通过 uv 提供的独立 Python 发行版创建环境，
避免依赖特定 Ubuntu 版本的 Python 安装包。定时任务使用 Python 3.11，自动跟进
补丁版本；测试覆盖 3.11 和 3.12。依赖通过 `pdm sync` 按 `pdm.lock` 安装，
定时任务只安装运行依赖。Python 系列停止支持后仍需升级，并先通过测试验证。

使用 [pdm](https://github.com/pdm-project/pdm) 来管理 virtualenv 和 dependencies。可以考虑使用[pipx](https://pypa.github.io/pipx/) 安装pdm

```sh
pdm install -G:all #安装依赖
make -j8 # 执行静态检查和测试
```

