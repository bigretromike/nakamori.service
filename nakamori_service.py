# -*- coding: utf-8 -*-

# TODO part1. for now we can exclude globalvars as we dont need them, until VideoLibrary is fixed
# TODO part2. but remember when you enable it on installation it will failed to run because it will start
# TODO part3. service before installing plugin and it will throw error from there.
# from nakamori_utils.globalvars import *
from nakamori_utils.script_utils import log_setsuzoku
from setsuzoku import Category, Action, Event

import lib.custom_monitor as cm
import lib.videolibrary_mapper as vl
import xbmc
import xbmcaddon
import time
import json


def handle_scrobbling():
    """
    Scrobbles the current position to Shoko and/or Trakt
    :return None:
    """
    pass


if __name__ == '__main__':
    # once per startup
    log_setsuzoku(Category.SERVICE, Action.MONITOR, Event.STARTUP)
    _last_call = int(time.time())
    last_call = int(xbmcaddon.Addon('service.nakamori').getSetting('last_call'))
    _last_sync_call = 0
    monitor = cm.CustomMonitor()

    while not monitor.abortRequested():
        s_watch = True if xbmcaddon.Addon('service.nakamori').getSetting('sv-watch') == 'true' else False
        s_rate = True if xbmcaddon.Addon('service.nakamori').getSetting('sv-rate') == 'true' else False

        # debug
        # vl.clean_videolibrary_scan()

        time_now = int(time.time())

        # once per hour
        if (time_now - _last_call) > 86400:
            _last_call = time_now
            log_setsuzoku(Category.SERVICE, Action.MONITOR, Event.CALL)

        # once per week
        if (time_now - last_call) > 604800:
            log_setsuzoku(Category.SYSTEM, Action.KODI, xbmc.getInfoLabel('System.BuildVersion'))

            # fix for busy from osversioninfo + future failsafe just in case
            _try = 0
            os_version = str(xbmc.getInfoLabel('System.OSVersionInfo'))
            while not vl.has_numbers(os_version) and _try <= 3:
                _try += 1
                xbmc.sleep(1000)
                os_version = str(xbmc.getInfoLabel('System.OSVersionInfo'))

            last_call = time_now
            xbmcaddon.Addon('service.nakamori').setSetting('last_call', '%s' % last_call)
            log_setsuzoku(Category.SYSTEM, Action.OS, os_version)

        # sync watch flag from shoko to videolibrary, once per hour
        if (time_now - _last_sync_call) > 86400:
            if s_watch or s_rate:
                vl.query_last_watched_episodes()
                vl.process_queue_of_watched_episodes()
                _last_sync_call = time_now

        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break

        # TODO part1. this service should monitor player activity
        # TODO part2. if it detects playing video we will check for shoko_exclusive parameters
        # TODO part3. if it detects that value it should check then handle status/marks to shoko
        # TODO part4. while doing it there should be a API endpoint to get info about latest watched episodes
        # TODO part5. so it can mark watched videos from outside kodi ecosystem so its sync with shoko
        # TODO part6. also it would be nice to have notification from ex. shoko that something was added
        # TODO part7. or other notification to maybe init a Library scan
        # TODO part8. or notification about upcoming events/episodes
