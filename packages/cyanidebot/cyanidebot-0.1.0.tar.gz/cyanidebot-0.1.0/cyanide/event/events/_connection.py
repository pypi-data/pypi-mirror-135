from typing import Any

from cyanide.event import Event, EventInfo, Intent


class ReadyEvent(Event):
    @staticmethod
    def get_event_info():
        return EventInfo("READY", Intent.DEFAULT)

    async def _parse_data(self, data: Any) -> Any:
        return ReadyEventData(data)


class ReadyEventData:
    _props: dict[str, Any]

    def __init__(self, props: dict[str, Any]):
        self._props = props

    @property
    def session(self) -> str:
        return self._props["session_id"]
