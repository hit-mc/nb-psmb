from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    psmb_host: str # PSMB Server
    psmb_port: int # PSMB Server port
    psmb_topic: str # 必须是ASCII字符串
    client_id: int # 客户端ID用来鉴别是否为自己，ID相同，则认为是同一个
    client_name: str # 客户端名，用来在MC服务端中写策略
    group_id: int # 对哪个群作出反应，群号
