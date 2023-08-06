# -*- coding: utf-8 -*-

from typing import List
from mod.common.component.baseComponent import BaseComponent

class HttpToWebServerCompServer(BaseComponent):
    def QueryLobbyUserItem(self, callback, playerId=None):
        # type: (function, str) -> None
        """
        查询还没发货的订单
        """
        pass

    def LobbyGetStorage(self, callback, playerId=None, keys=None):
        # type: (function, str, List[str]) -> None
        """
        获取存储的数据
        """
        pass

    def LobbySetStorageAndUserItem(self, callback, playerId=None, orderId=None, entities=None):
        # type: (function, str, int, List[dict]) -> None
        """
        设置订单已发货或者存数据
        """
        pass

