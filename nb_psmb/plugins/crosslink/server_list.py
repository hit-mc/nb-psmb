import asyncio

from loguru import logger

from hitmc_messages import (Message,
                            MessageType,
                            Dispatcher,
                            PlayerListResponseMessage)
from psmb_client.guardian import Guardian
from nonebot import get_bot


class ServerListDaemon:
    def __init__(self, base_msg: Message, client: Guardian, dispatcher: Dispatcher, group_id) -> None:
        self._base_msg = base_msg
        self._client = client
        self._dispacher = dispatcher
        self._result = {}
        self._group_id = group_id
        dispatcher.add_message_listener(
            MessageType.PLAYER_LIST_RESPONSE, self.recv_list)

    def recv_list(self, msg: PlayerListResponseMessage):
        self._result[msg.client_name] = msg.online_players

    async def server_list(self, wait_time: float = 1.):
        self._result = {}
        request_model = Message(**self._base_msg.dict())
        request_model.msg_type = MessageType.PLAYER_LIST_REQUEST
        try:
            await self._client.send_msg(request_model.json().encode('utf-8'))
        except RuntimeError:
            pass
        except Exception as exception:
            logger.warning(f"Uncaught exception {exception!r}")
        await asyncio.sleep(wait_time)
        bot = get_bot()
        ok = False
        for k, v in self._result.items():
            msg = f"[{k}]\n" + ', '.join(v)
            if len(v) != 0:
                await bot.send_group_msg(group_id=self._group_id, message=msg)
                ok = True
        if not ok:
            msg = '[鬼服]\n目前没有玩家上线'
            await bot.send_group_msg(group_id=self._group_id, message=msg)
