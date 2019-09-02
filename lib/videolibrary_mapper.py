# -*- coding: utf-8 -*-
import xbmc
import json
import series_map
import episodes_map


def kodi_rpc(method, params, limits=''):
    json_id += 1
    jsonrpc = '{"jsonrpc":"2.0","id":%d,"method":"%s","params":{%s} %s}' % (json_id, method, params, limits)
    xbmc.log(' -----------> rpc (send): %s' % jsonrpc, xbmc.LOGNOTICE)
    rpc = xbmc.executeJSONRPC(jsonrpc)
    xbmc.log(' -----------> rpc (recv): %s' % jsonrpc, xbmc.LOGNOTICE)
    rpc = json.loads(rpc)
    return rpc


def clean_videolibrary_scan():
    xbmc.log('====> VideoLibrary Scan: Start <====', xbmc.LOGNOTICE)
    index_start = 0
    index_stop = 10
    index_count = 100
    while index_stop < index_count:
        xbmc.log('=====> series : %s -- %s / %s' % (index_start, index_stop, index_count), xbmc.LOGNOTICE)
        results = kodi_rpc('VideoLibrary.VideoLibrary.GetEpisodes', '"properties":["tvshowid", "title","uniqueid"]', ',"limits": {"start": %d,"end": %d}' % (index_start, index_stop))
        if 'result' not in results:
            break
        index_start = results['result']['limits'].get('start', 0)
        index_stop = results['result']['limits'].get('end', 0)
        index_count = results['result']['limits'].get('total', 0)

        for tvshows in results.get('episodes', []):
            tid = tvshows.get('tvshowid', 0)
            eid = tvshows.get('episodeid', 0)
            said = 0  # shoko_aid
            seid = 0  # shoko_eid
            aaid = 0  # anidb_aid
            aeid = 0  # anidb_eid
            if 'uniqueid' in tvshows:
                if 'shoko_aid' in tvshows['uniqueid'] and 'shoko_eid' in tvshows['uniqueid']:
                    said = tvshows['uniqueid'].get('shoko_aid', 0)
                    seid = tvshows['uniqueid'].get('shoko_eid', 0)
                    # not supported
                    aaid = tvshows['uniqueid'].get('anidb_aid', 0)
                    aeid = tvshows['uniqueid'].get('anidb_eid', 0)
            if tid > 0 and eid > 0 and said > 0 and seid > 0:
                if not series_map.check(tid=tid, aid=aaid, sid=said):
                    series_map.add_map(tid=tid, aid=aaid, sid=sid)
                if not episodes_map.check(vlid=eid, eid=aeid, sid=seid):
                    episodes_map.add_map(vlid=eid, eid=aeid, sid=seid)

        index_step = index_stop - index_start
        index_start = index_stop
        index_stop += index_step

    xbmc.log('====> VideoLibrary Scan: Finish', xbmc.LOGNOTICE)
