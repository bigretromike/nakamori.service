# -*- coding: utf-8 -*-
import xbmc
import json


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

    def onDatabaseScanStarted(self, database):
        xbmc.log('onDatabaseScanStarted', xbmc.LOGNOTICE)
        xbmc.log(str(database), xbmc.LOGNOTICE)

    def onDatabaseUpdated(self, database):
        xbmc.log('onDatabaseUpdated', xbmc.LOGNOTICE)
        xbmc.log(str(database), xbmc.LOGNOTICE)

    def onCleanFinished(self, library):
        xbmc.log('onCleanFinished', xbmc.LOGNOTICE)
        xbmc.log(str(library), xbmc.LOGNOTICE)

    def onCleanStarted(self, library):
        xbmc.log('onCleanStarted', xbmc.LOGNOTICE)
        xbmc.log(str(library), xbmc.LOGNOTICE)

    def onAbortRequested(self):
        xbmc.log('onAbortRequested', xbmc.LOGNOTICE)

    def onNotification(self, sender, method, data):
        xbmc.log('onNotification', xbmc.LOGNOTICE)

        if method == 'VideoLibrary.OnUpdate':
            response = json.loads(data)
            if 'item' in response and 'type' in response['item'] and response.get('item').get('type') == 'episode':
                playcount = response['playcount']
                episode_id = str(response['item']['id'])
                rpc = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["file", "productioncode"], "episodeid": ' + episode_id + '}, "id": 1 }')
                rpc_json = json.loads(rpc)
                if 'episodedetails' in rpc_json['result'] and 'file' in rpc_json['result'].get('episodedetails'):
                    file = rpc_json['result'].get('episodedetails').get('file')
                    if 'plugin.video.nakamori' in file:
                        file = file.replace('plugin://plugin.video.nakamori/tvshows/', '')
                        file = file.replace('/play', '')
                        ep_id = int(file)
                        watch_flag = True if playcount == 1 else False
                        xbmc.executebuiltin("RunScript(script.module.nakamori,/episode/%s/set_watched/%s)" % (ep_id, watch_flag))
                    else:
                        # not our file
                        pass
        # full list of all method that we could use (excluding AudioLibrary)
        # https://github.com/xbmc/xbmc/blob/master/xbmc/interfaces/json-rpc/schema/notifications.json
        # some of them does duplication as Monitor functions that get trigger
        # not sure if all or where its better to handle them :-)
        elif method in {"Player.OnPlay",
                        "Player.OnResume",
                        "Player.OnAVStart",
                        "Player.OnAVChange",
                        "Player.OnPause",
                        "Player.OnStop",
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
            pass
