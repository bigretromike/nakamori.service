# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import json
# from nakamori_utils import script_utils
import library_map as map
# addon = xbmcaddon.Addon('service.nakamori')


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
        xbmc.log('Found data: %s' % data, xbmc.LOGNOTICE)
        xbmc.log('Found method: %s' % method, xbmc.LOGNOTICE)

        if method == 'VideoLibrary.OnUpdate':
            response = json.loads(data)
            xbmc.log('Found response: %s' % response, xbmc.LOGNOTICE)
            # TODO UpdateLibrary is broken because missing info: https://github.com/xbmc/xbmc/issues/16245

            # if 'item' in response and 'type' in response['item'] and response.get('item').get('type') == 'episode':
            #     playcount = response.get('playcount', -1)
            #     episode_id = int(response['item'].get('id', 0))
            #     # this event get trigger while adding items from video source
            #     if episode_id > 0 and playcount != -1:
            #         rpc = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["file", "productioncode"], "episodeid": %s}, "id": 1 }' % episode_id)
            #         rpc_json = json.loads(rpc)
            #         if 'episodedetails' in rpc_json['result'] and 'file' in rpc_json['result'].get('episodedetails'):
            #             file = rpc_json['result'].get('episodedetails').get('file')
            #             if 'plugin.video.nakamori' in file:
            #                 file = file.replace('plugin://plugin.video.nakamori/tvshows/', '')
            #                 file = file.replace('/play', '')
            #                 ep_id = int(file)
            #                 watch_flag = True if playcount == 1 else False
            #                 xbmc.executebuiltin("RunScript(script.module.nakamori,/episode/%s/set_watched/%s)" % (ep_id, watch_flag))
            #             else:
            #                 # not our file
            #                 pass

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
            pass
        elif method in {"Player.OnAVChange", "Player.OnPlay"}:
            response = json.loads(data)
            xbmc.log('Found (OnPlay) response: %s' % response, xbmc.LOGNOTICE)

            # playerid = -1
            # rpc = xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":33,"method":"Player.GetActivePlayers","params":{}}')
            # rpc = json.loads(rpc)
            # xbmc.log('1 ----------- rpc response: %s' % rpc, xbmc.LOGNOTICE)
            # # get current playerid, should be 1, but who know
            # while len(rpc.get('result', [])) == 0:
            #     xbmc.sleep(100)
            #     rpc = xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":33,"method":"Player.GetActivePlayers","params":{}}')
            #     rpc = json.loads(rpc)
            #     xbmc.log('2 ----------- rpc response: %s' % rpc, xbmc.LOGNOTICE)

            # xbmc.log('3 ----------- rpc response: %s' % rpc, xbmc.LOGNOTICE)
            # for player in rpc['result']:
            #     xbmc.log('4 ----------- player: %s' % player, xbmc.LOGNOTICE)
            #     xbmc.log('4.5 ---------- %s %s ' % (player['type'], player['playerid']), xbmc.LOGNOTICE)
            #     if player.get('type', 'video') == 'video':
            #         playerid = int(player['playerid'])

            # xbmc.log('5 ----------- playerid: %s' % playerid, xbmc.LOGNOTICE)
            # # get information about played file
            # shoko_eid = -1
            # shoko_aid = -1
            # is_in_vl = False
            # if playerid != -1:
            #     rpc = xbmc.executeJSONRPC('{"jsonrpc":"2.0","id":40,'
            #                               '"method":"Player.GetItem",'
            #                               '"params":{"playerid":%s,"properties":["showtitle","title","episode",'
            #                               '"season","uniqueid","playcount","lastplayed","userrating","tvshowid","file",'
            #                               '"mediapath"]}}' % playerid)
            #     rpc = json.loads(rpc)
            #     xbmc.log('6 ----------- rpc: %s' % rpc, xbmc.LOGNOTICE)

            #     if 'result' in rpc:
            #         if 'item' in rpc['result']:
            #             item = rpc['result'].get('item', '[]')
            #             showtitle = item.get('showtitle', '')
            #             title = item.get('title', '')
            #             showtype = item.get('type', 'episode')
            #             episode = item.get('episode', '-1')
            #             season = item.get('season', '-1')
            #             file_node = item.get('file', '')
            #             if "plugin.video.nakamori/episode/" in file_node and "/file/0/play" in file_node:
            #                 is_in_vl = True
            #             elif '/Stream/' in file_node and '/False/file.mkv' in file_node:
            #                 is_in_vl = False

            #             if 'uniqueid' in item:
            #                 if 'shoko_eid' in item['uniqueid']:
            #                     shoko_eid = item['uniqueid'].get('shoko_eid', -1)
            #                     shoko_aid = item['uniqueid'].get('shoko_aid', -1)

            #             xbmc.log('-----> %s %s %s %s %s %s' % (showtitle, title, showtype, episode, season, file_node), xbmc.LOGNOTICE)

            #             if shoko_eid != -1 and shoko_aid != -1:
            #                 xbmc.log('----->>>> %s' % map.get_data_from_map(file_node), xbmc.LOGNOTICE)
            #                 if map.get_data_from_map(filename=file_node) is None:
            #                     map.add_map(showtitle, title, showtype, episode, season, file_node, shoko_eid, str(is_in_vl))


                    #if is_in_vl:
                    #    # TODO from VL to shoko
                    #    if addon.getSetting("vs_watch") == 'true':
                    #        script_utils.url_series_watched_status(self.id, True)
                    #        pass
                    #    if addon.getSetting("vs_rate") == 'true':
                    #        pass
                    #else:
                    #    # TODO from Shoko to VL
                    #    if addon.getSetting("sv_watch") == 'true':
                    #        pass
                    #    if addon.getSetting("sv_rate") == 'true':
                    #        pass

            # send proper mark in proper direction

        elif method in {"Player.OnStop"}:
            # xbmc.log('->>>>>>>>> DATA (OnStop): %s' % data, xbmc.LOGNOTICE)
            # response = json.loads(data)
            # xbmc.log('->>>>>>>>> RESPONS (OnStop): %s' % response, xbmc.LOGNOTICE)

            # showtitle = response['item'].get('showtitle', '')
            # title = response['item'].get('title', '')
            # showtype = response['item'].get('type', 'episode')
            # episode = response['item'].get('episode', '-1')
            # season = response['item'].get('season', '-1')
            # row = map.get_data_from_map(showtitle, title, showtype, episode, season)
            # xbmc.log('MAP: %s %s %s %s %s' % (showtitle, title, showtype, episode, season), xbmc.LOGNOTICE)

            # xbmc.log('->>>>>>>>> ROW (OnStop): %s' % row, xbmc.LOGNOTICE)
            pass
