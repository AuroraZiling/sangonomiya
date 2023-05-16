import asyncio
import os

from PySide6.QtCore import Signal, QThread
from enkanetwork import EnkaNetworkAPI

from ...Scripts.Utils import downloader
from ...Scripts.Utils.tools import Tools

utils = Tools()
client = EnkaNetworkAPI(lang="chs")
uid = ""
result = {"nickname": "正在获取...", "level": "正在获取...",
          "icon_url": "正在获取...", "signature": "正在获取...",
          "achievement": "正在获取...",
          "abyss_floor": "正在获取..."}


class AccountGetInfoThread(QThread):
    trigger = Signal(dict)

    def __init__(self, getUid, parent=None):
        super(AccountGetInfoThread, self).__init__(parent)
        global uid
        uid = getUid

    def run(self):
        self.trigger.emit(result)
        asyncio.run(connectENKA())
        if not os.path.exists(f"{utils.workingDir}/cache/{result['icon_url'].split('/')[-1]}"):
            downloader.downloadFromImage(result["icon_url"], f"{utils.workingDir}/cache/", result["icon_url"].split('/')[-1])
        self.trigger.emit(result)


async def connectENKA():
    async with client:
        global result
        data = await client.fetch_user(uid)
        result = {"nickname": data.player.nickname, "level": data.player.level,
                  "icon_url": data.player.avatar.icon.url, "signature": data.player.signature,
                  "achievement": data.player.achievement, "abyss_floor": f"{data.player.abyss_floor}-{data.player.abyss_room}"}