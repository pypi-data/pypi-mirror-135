from typing import Any

from cyanide.event import Event, EventInfo, Intent
from cyanide.model.message import Message


class _MessageReceivedEvent(Event):
    async def _parse_data(self, data: dict[str, Any]):
        return Message.from_dict(self._bot, data)


class ChannelMessageReceivedEvent(_MessageReceivedEvent):
    """
    当接收到子频道用户所发送含提及机器人消息时触发。

    触发时回调的数据类型为 `Message`。
    """

    @staticmethod
    def get_event_info():
        return EventInfo("AT_MESSAGE_CREATE", Intent.MENTION)
