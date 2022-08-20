# nonebot PSMB 客户端

## 配置文件

.env.example 中给出了示例配置。自行修改为适合自用的配置后，重命名为 .env.prod。

```env
HOST=0.0.0.0                    # 监听的地址 (为 go-cqhttp 服务的)
PORT=8080                       # 监听端口，需要和 psmb 中配置一致
PSMB_HOST=127.0.0.1             # PSMB 服务器地址
PSMB_PORT=13880                 # PSMB 服务器端口
CLIENT_ID=1                     # 客户端 ID， 唯一字段， PSMB 的一部分
CLIENT_NAME=qqbot               # 客户端名字，可以不唯一
PSMB_ID_PATTERN=topic           # 从 QQ 群里发给 PSMB 的 topic
PSMB_TOPIC=topic                # 我们需要接收的 topic
GROUP_ID=123456                 # 群号
ENABLE_TLS=false                # 是否启用传输层安全协议
```

## 依赖

推荐在一个虚拟环境中安装依赖。

```zsh
pip install -r requirements.txt
```


### 运行


```zsh
python bot.py
```
