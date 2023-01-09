# hzj-sign

慧职教签到

## 配置文件

创建或编辑 `config.json` 文件

![image](https://user-images.githubusercontent.com/28248888/211381066-09ce1a18-fd69-4287-95cc-e3c11e6bedc5.png)

| 字段       | 说明                        |
|----------|---------------------------|
| sign     | 签到配置                      |
| pushplus | 可空，[PushPlus] 消息推送的 Token |

### `sign` 签到配置

| 字段           | 说明                                           |
|--------------|----------------------------------------------|
| url          | 学校服务器链接                                      |
| token        | 账号凭证                                         |
| trip         | 是否出差，默认 `false`                              |
| address      | 可空，中文地址                                      |
| x            | 可空，经度                                        |
| y            | 可空，纬度                                        |
| studentId    | 可空，学生 id                                     |
| internshipId | 可空，实习 id                                     |
| checkType    | 可空，签到类型：<br>`CHECKIN` 签到（默认）<br>`SIGNOFF` 签退 |
| attachIds    | 可空，附件 id                                     |

### 从浏览器控制台获取配置

登录：http://gzdk.gzisp.net/hzjmui/mui/login.html  
执行 [console.js](./console.js) 里的内容

### 经纬度

可通过 https://tool.lu/coordinate/ 获取。

### 定时执行

搜索引擎搜索，自行配置：`crontab`、`windows 计划任务`、`宝塔计划任务` 等。

[PushPlus]: https://www.pushplus.plus/
