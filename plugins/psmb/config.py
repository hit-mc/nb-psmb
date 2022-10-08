from typing import Mapping
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    psmb_host:              str     # PSMB Server
    psmb_port:              int     # PSMB Server port
    psmb_topic:             str     # 必须是ASCII字符串
    client_id:              int     # 客户端ID用来鉴别是否为自己，ID相同，则认为是同一个
    client_name:            str     # 客户端名，用来在MC服务端中写策略
    group_server_mapping:   Mapping  # 对频道消息和服务器消息的映射
