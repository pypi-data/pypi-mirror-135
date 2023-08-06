from __future__ import annotations

from collections import defaultdict
from typing import ItemsView, KeysView, ValuesView

HOST = 'Host'
UPGRADE = 'Upgrade'
CONNECTION = 'Connection'
SEC_WEBSOCKET_KEY = 'Sec-WebSocket-Key'
SEC_WEBSOCKET_ACCEPT = 'Sec-WebSocket-Accept'
SEC_WEBSOCKET_VERSION = 'Sec-WebSocket-Version'


class HTTPHeaders:
    def __init__(self):
        self._map: dict[str, list[str]] = defaultdict(list)

    def __getitem__(self, key: str) -> list[str]:
        return self._map[key.lower()]

    def __setitem__(self, key: str, value: str) -> None:
        self._map[key.lower()].append(value)

    def __delitem__(self, key: str) -> None:
        del self._map[key.lower()]

    def keys(self) -> KeysView[str]:
        return self._map.keys()

    def value(self) -> ValuesView[list[str]]:
        return self._map.values()

    def items(self) -> ItemsView[str, list[str]]:
        return self._map.items()

    def get(self, key: str, default: str = '') -> list[str]:
        return self._map.get(key.lower(), [default])

    def getone(self, key: str, default: str = ''):
        return self.get(key, default)[0]
