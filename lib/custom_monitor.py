# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import json
import videolibrary_mapper
import episodes_map as e_map


# updated to v19 list, removed deprecated
class CustomMonitor(xbmc.Monitor):
    def __init__(self):
        super(CustomMonitor, self).__init__()

    def onSettingsChanged(self):
        xbmc.log('onSettingsChanged', xbmc.LOGNOTICE)

    def onScreensaverActivated(self):
        xbmc.log('onScreensaverActivated', xbmc.LOGNOTICE)

    def onScreensaverDeactivated(self):
        xbmc.log('onScreensaverDeactivated', xbmc.LOGNOTICE)

    def onDPMSActivated(self):
        xbmc.log('onDPMSActivated', xbmc.LOGNOTICE)

    def onDPMSDeactivated(self):
        xbmc.log('onDPMSDeactivated', xbmc.LOGNOTICE)

    def onScanStarted(self, library):
        xbmc.log('onScanStarted', xbmc.LOGNOTICE)
        xbmc.log(str(library), xbmc.LOGNOTICE)

    def onScanFinished(self, library):
        xbmc.log('onScanFinished', xbmc.LOGNOTICE)
        xbmc.log(str(library), xbmc.LOGNOTICE)

        # if scan for new content is finish lets iterate all items and map them to shoko internal id's
        v_watch = True if xbmcaddon.Addon('service.nakamori').getSetting('vs-watch') == 'true' else False
        v_rate = True if xbmcaddon.Addon('service.nakamori').getSetting('vs-rate') == 'true' else False
        if v_watch or v_rate:  # let's not slow down LibraryScanning for does using only Plugin
            videolibrary_mapper.clean_videolibrary_scan()

    def onCleanStarted(self, library):
        xbmc.log('onCleanStarted', xbmc.LOGNOTICE)
        xbmc.log(str(library), xbmc.LOGNOTICE)

    def onCleanFinished(self, library):
        xbmc.log('onCleanFinished', xbmc.LOGNOTICE)
        xbmc.log(str(library), xbmc.LOGNOTICE)

    def onAbortRequested(self):
        xbmc.log('onAbortRequested', xbmc.LOGNOTICE)

    def onNotification(self, sender, method, data):
        xbmc.log('onNotification', xbmc.LOGNOTICE)
        xbmc.log('Found data: %s' % data, xbmc.LOGNOTICE)
        xbmc.log('Found method: %s' % method, xbmc.LOGNOTICE)

        # sync VL watched flag with shoko
        if method == 'VideoLibrary.OnUpdate':
            response = json.loads(data)
            xbmc.log('Found response: %s' % response, xbmc.LOGNOTICE)
            # TODO UpdateLibrary is broken because missing info: https://github.com/xbmc/xbmc/issues/16245
            # TODO its broken for anything played outside VideoLibrary

            # read setting each time, because we dont want to force restart
            v_watch = True if xbmcaddon.Addon('service.nakamori').getSetting('vs-watch') == 'true' else False
            v_rate = True if xbmcaddon.Addon('service.nakamori').getSetting('vs-rate') == 'true' else False

            if 'item' in response:
                # {u'item': {u'type': u'episode', u'id': 6}, u'transaction': True}  <- when adding to db
                # {u'item': {u'type': u'episode', u'id': 6}, u'added': True, u'transaction': True}  <- when adding to db
                if 'transaction' not in response['item'] and 'added' not in response['item']:
                    # {u'item': {u'type': u'episode', u'id': 6}, u'playcount': 1}
                    if v_watch:
                        if 'type' in response['item'] and response.get('item').get('type') == 'episode':
                            playcount = response.get('playcount', -1)
                            episode_id = int(response['item'].get('id', 0))

                            if episode_id > 0 and playcount != -1:
                                shoko_eid = e_map.get(vlid=episode_id)
                                if shoko_eid is not None:
                                    shoko_eid = shoko_eid[2]
                                    watch_flag = True if playcount == 1 else False
                                    xbmc.log(' ==> vl_sync: TRIGGER WATCH for %s - %s' % (shoko_eid, watch_flag), xbmc.LOGNOTICE)
                                    xbmc.executebuiltin("RunScript(script.module.nakamori,/episode/%s/set_watched/%s)" % (shoko_eid, watch_flag))

        elif method in {"Player.OnAVChange", "Player.OnPlay"}:
            response = json.loads(data)
            xbmc.log('Found (OnPlay) response: %s' % response, xbmc.LOGNOTICE)

        elif method in {"Player.OnStop"}:
            pass

        # full list of all method that we could use (excluding AudioLibrary)
        # https://github.com/xbmc/xbmc/blob/master/xbmc/interfaces/json-rpc/schema/notifications.json
        # some of them does duplication as Monitor functions that get trigger
        # not sure if all or where its better to handle them :-)
        elif method in {"Player.OnResume",
                        "Player.OnPause",
                        "Player.OnSpeedChanged",
                        "Player.OnSeek",
                        "Player.OnPropertyChanged",
                        "Playlist.OnAdd",
                        "Playlist.OnRemove",
                        "Playlist.OnClear",
                        "VideoLibrary.OnExport",
                        "VideoLibrary.OnRemove",
                        "VideoLibrary.OnScanStarted",
                        "VideoLibrary.OnScanFinished",
                        "VideoLibrary.OnCleanStarted",
                        "VideoLibrary.OnCleanFinished",
                        "VideoLibrary.OnRefresh",
                        "System.OnQuit",
                        "System.OnRestart",
                        "System.OnSleep",
                        "System.OnWake",
                        "System.OnLowBattery",
                        "Application.OnVolumeChanged",
                        "GUI.OnScreensaverActivated",
                        "GUI.OnScreensaverDeactivated",
                        "GUI.OnDPMSActivated",
                        "GUI.OnDPMSDeactivated"
                        }:
            # we don't need those
            pass
