#-*- coding:utf-8 -*-
import os
from .base import Comparer
from .base import Condition
from ..torrentstatus import TorrentStatus

class HardLinkCondition(Condition):
    def __init__(self, r, comp = Comparer.GT):
        Condition.__init__(self) # Initialize remain and remove list
        self._hardlink = r
        self._comparer = comp

    def apply(self, client_status, torrents):
        for torrent in torrents:
            hardlinks = sum(
                os.stat(os.path.join(root, file)).st_nlink - 1
                for root, _, files in os.walk(torrent.content_path)
                for file in files
                if os.stat(os.path.join(root, file)).st_nlink > 1
            )
            if self.compare(hardlinks, self._hardlink, self._comparer):
                self.remove.add(torrent)
            else:
                self.remain.add(torrent)