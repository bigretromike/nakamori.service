# -*- coding: utf-8 -*-
import xbmc
import json
import series_map as series
import episodes_map as episodes
import sync_helper as sync
from datetime import date
from proxy.python_version_proxy import python_proxy as pyproxy


def kodi_rpc(method, params, limit='', json_id=0):
    json_id += 1
    jsonrpc = '{"jsonrpc":"2.0","id":%d,"method":"%s","params":{%s}%s}' % (json_id, method, params, limit)
    xbmc.log(' -----------> rpc (send): %s' % jsonrpc, xbmc.LOGNOTICE)
    rpc = xbmc.executeJSONRPC(jsonrpc)
    xbmc.log(' -----------> rpc (recv): %s' % rpc, xbmc.LOGNOTICE)
    rpc = json.loads(rpc)
    return rpc


def clean_videolibrary_scan():
    xbmc.log('====> VideoLibrary Scan: Start <====', xbmc.LOGNOTICE)
    index_start = 0
    index_stop = 10
    index_count = 100
    json_id = 0
    while index_stop < index_count:
        xbmc.log('=====> series : %s -- %s / %s' % (index_start, index_stop, index_count), xbmc.LOGNOTICE)
        results = kodi_rpc('VideoLibrary.GetEpisodes',
                           '"properties":["tvshowid","title","uniqueid"]',
                           ',"limits":{"start":%d,"end":%d}' % (index_start, index_stop),
                           json_id)

        if 'result' not in results:
            xbmc.log('====> no result found <====', xbmc.LOGNOTICE)
            break
        json_id = int(results['id'])
        index_start = results['result']['limits'].get('start', 0)
        index_stop = results['result']['limits'].get('end', 0)
        index_count = results['result']['limits'].get('total', 0)

        for tvshows in results['result'].get('episodes', []):
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
                    aaid = tvshows['uniqueid'].get('anidb_aid', 0)
                    aeid = tvshows['uniqueid'].get('anidb_eid', 0)
                xbmc.log(' ====> uniqueid: %s => %s => %s, %s => %s => %s' % (tid, said, aaid, eid, seid, aeid), xbmc.LOGNOTICE)
            if tid > 0 and eid > 0 and said > 0 and seid > 0:
                if not series.check(tid=tid, aid=aaid, sid=said):
                    series.add_map(tid=tid, aid=aaid, sid=said)
                    xbmc.log(' ====> add_series: %s => %s, %s' % (tid, aaid, said), xbmc.LOGNOTICE)
                if not episodes.check(vlid=eid, eid=aeid, sid=seid):
                    episodes.add_map(vlid=eid, eid=aeid, sid=seid)
                    xbmc.log(' ====> add_episod: %s => %s, %s' % (eid, aeid, seid), xbmc.LOGNOTICE)

        index_step = index_stop - index_start
        index_start = index_stop
        index_stop += index_step

    xbmc.log('====> VideoLibrary Scan: Finish', xbmc.LOGNOTICE)


def query_last_watched_episodes():
    xbmc.log('====> query_last_watched_episodes', xbmc.LOGNOTICE)
    from nakamori_utils.globalvars import server
    # [{"type":"ep","view":1,"view_date":"2019-09-03T13:42:36.9194063+02:00","eptype":"Episode","epnumber":10,"aid":14662,"eid":219322,"id":74,"name":"Episode 10","summary":"Episode Overview not Available","year":"2019","air":"2019-09-02","rating":"2.80","votes":"1","art":{}}]
    today = date.today().strftime("%Y-%m-%d")
    offset = 0
    limit = 100  # setting without limit results in loop
    url = server + '/api/ep/last_watched?query=%s&limit=%s&offset=%s' % (today, limit, offset)
    xbmc.log('====> url: %s' % url, xbmc.LOGNOTICE)
    x = pyproxy.get_json(url, True)
    if x is not None and len(x) > 2:  # []
        x = json.loads(x)
        while len(x) > 0:
            for y in x:
                if isinstance(y, dict):
                    xbmc.log('====> query_last_watched_episodes x: %s %s' % (type(y), y), xbmc.LOGNOTICE)
                    watch_date = y.get('view_date', '')
                    aid = y.get('aid', 0)
                    eid = y.get('eid', 0)
                    shoko_eid = y.get('id', 0)
                    sync.add_to_queue(aid, eid, shoko_eid)

            offset = offset + limit
            url = server + '/api/ep/last_watched?query=%s&limit=%s&offset=%s' % (today, limit, offset)
            xbmc.log('====> url: %s' % url, xbmc.LOGNOTICE)
            x = pyproxy.get_json(url, True)
            if x is None:
                break
            if x == '[]':
                break

    # finish checking
    sync.add_date(today)


def process_queue_of_watched_episodes():
    queue = sync.get_queue()
    for q in queue:
        shoko_eid = q[2]
        a_eid = q[1]
        a_aid = q[0]
        vl_ep_id = episodes.get(eid=a_eid, sid=shoko_eid)
        if vl_ep_id is not None:
            vl_ep_id = vl_ep_id[0]
            # we found mapping
            xbmc.log('===> process_queue_of_watched_episodes vl_ep_id: %s' % vl_ep_id, xbmc.LOGNOTICE)
            r = kodi_rpc('VideoLibrary.GetEpisodeDetails', '"episodeid": %s,"properties":["playcount"]' % vl_ep_id)
            if 'result' in r and 'episodedetails' in r['result']:
                if r['result']['episodedetails']['playcount'] == 0:
                    m = kodi_rpc('VideoLibrary.SetEpisodeDetails', '"episodeid":%s,"playcount": 1' % vl_ep_id)
                    if m.get('result', '') == "OK":
                        xbmc.log('===> mark watched %s - OK' % vl_ep_id, xbmc.LOGNOTICE)
        else:
            xbmc.log('----> missing mapping ! %s %s %s <----' % (a_aid, a_eid, shoko_eid), xbmc.LOGNOTICE)
    # try to clear queue
    return sync.clear_queue(len(queue))


def has_numbers(input):
    return any(char.isdigit() for char in input)
