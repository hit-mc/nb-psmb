import asyncio
import re

from nonebot import get_driver
from nonebot.adapters import Event
from nonebot import on_message, get_bot
from hitmc_messages import (
    PlayerChatMessage,
    Message,
    PlayerAdvancementMessage,
    MessageType,
    PlayerDeathMessage,
    Dispatcher
)

from psmb_client.guardian import Guardian
from loguru import logger

from .config import Config
from .server_list import ServerListDaemon

nb_message = on_message()
driver = get_driver()
plugin_config = Config.parse_obj(get_driver().config)
dispatcher = Dispatcher()


async def feed_packet(packet: bytes):
    return dispatcher.feed_packet(packet)


client: Guardian = Guardian(
    plugin_config.psmb_host,
    plugin_config.psmb_port,
    plugin_config.psmb_topic,
    plugin_config.client_id,
    feed_packet
)

base_msg = Message(
    client_name=plugin_config.client_name,
    client_id=plugin_config.client_id,
    msg_type=MessageType.PLAYER_CHAT,
    content=''
)

server_list_daemon = ServerListDaemon(
    base_msg,
    client, dispatcher,
    plugin_config.group_server_mapping
)


def format_chat(pcm: PlayerChatMessage):
    return '[{}]<{}> {}'.format(pcm.client_name, pcm.player_name, pcm.content)


@dispatcher.on(MessageType.PLAYER_CHAT)
def _(msg: PlayerChatMessage):
    if msg.client_id == plugin_config.client_id:
        return
    bot = get_bot()
    if msg.content.startswith(('!', '！')):
        return
    asyncio.create_task(
        bot.send_group_msg(
            group_id=plugin_config.group_id,
            message=format_chat(msg)
        )
    )


@dispatcher.on(MessageType.PLAYER_DEATH)
def _(msg: PlayerDeathMessage):
    bot = get_bot()
    msg1 = '[悲报]<{}> {}'.format(msg.client_name, msg.content)
    msg2 = '[x:%.0f, y:%.0f, z:%.0f, dim: %s]' % (
        msg.death_position + (msg.death_dim,))
    asyncio.create_task(bot.send_group_msg(
        group_id=plugin_config.group_id, message=msg1))
    asyncio.create_task(bot.send_group_msg(
        group_id=plugin_config.group_id, message=msg2))


@dispatcher.on(MessageType.PLAYER_ADVANCEMENT)
def _(msg: PlayerAdvancementMessage):
    bot = get_bot()
    m = '[喜报] {}'.format(msg.content)
    asyncio.create_task(bot.send_group_msg(
        group_id=plugin_config.group_id, message=m))


@driver.on_startup
async def _():
    await client._try_connect()


@driver.on_shutdown
async def _():
    await client.close()


async def parse_command(msg: str):
    if msg == '#!list':
        await server_list_daemon.server_list()
        return


@nb_message.handle()
async def _(event: Event):
    msg_content = str(event.get_message())
    if event.get_session_id().find(str(plugin_config.group_id)) == -1:
        return
    if msg_content.startswith('#!'):
        await parse_command(msg_content)
        return
    sender = event.sender.card  # type: ignore
    if sender is None or sender == '':
        sender = event.sender.nickname  # type: ignore
    # 删除CQ码
    msg_content = re.sub(r'\[CQ:.*\]', '', msg_content)
    if len(msg_content) == 0:
        return
    msg = PlayerChatMessage(**base_msg.dict(),
                            player_name=sender)
    msg.content = msg_content
    msg.msg_type = MessageType.PLAYER_CHAT
    try:
        await client.send_msg(msg.json().encode('utf-8'))
    except RuntimeError:
        pass
    except Exception as exception:
        logger.warning(f"Uncaught exception {exception!r}")
