#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xbmc

from nakamori_utils.globalvars import *


def handle_scrobbling():
    """
    Scrobbles the current position to Shoko and/or Trakt
    :return None:
    """
    pass


if __name__ == '__main__':
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        # Sleep/wait for abort for 2 seconds
        if monitor.waitForAbort(2):
            # Abort was requested while waiting. We should exit
            break

        # we are running, check the players for relevant playback
        player = xbmc.Player()
        if not player.isPlayingVideo():
            continue

        playing_file = player.getPlayingFile()
        if playing_file is None or server not in playing_file:
            continue

        handle_scrobbling()
