# hzj-sign

慧职教签到

## 配置文件

创建或编辑 `config.json` 文件

| 字段       | 说明                        |
|----------|---------------------------|
| token    | 账号凭证                      |
| trip     | 是否出差，默认 `false`           |
| address  | 可空，中文地址                   |
| location | 可空，经纬度                    |
| pushplus | 可空，[PushPlus] 消息推送的 Token |

### `token` 账号凭证

登录 http://gzdk.gzisp.net/hzjmui/mui/login.html 后，  
按 `F12` 调出 `开发者工具`，查看 `应用` - `会话存储空间` 里的 `token` 值。  
或在 `控制台` 中执行 `sessionStorage.token` 查看。

### `location` 经纬度

如：`116.422522-39.901873`，可通过 https://tool.lu/coordinate/ 获取。

[PushPlus]: https://www.pushplus.plus/

### 定时执行

搜索引擎搜索，自行配置：`crontab`、`windows 计划任务`、`宝塔计划任务` 等。
