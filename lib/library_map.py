# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import xbmcaddon, xbmc, os
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
else:
    addon = xbmcaddon.Addon('service.nakamori')
    profileDir = addon.getAddonInfo('profile')
    profileDir = xbmc.translatePath(profileDir)
    if not os.path.exists(profileDir):
        os.makedirs(profileDir)
    db_file = os.path.join(profileDir, 'map.db')
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute('CREATE TABLE IF NOT EXISTS [library_map] ([showtitle] TEXT NULL, [title] TEXT NULL, [showtype] TEXT NULL, [episode] TEXT NULL, [season] TEXT NULL, [filename] TEXT NULL, [shoko_eid] TEXT NULL, [direction] TEXT NULL, [created] FLOAT NULL);')
    except:
        pass

db_connection.close()

def add_map(showtitle, title, showtype, episode, season, filename, shoko_eid, direction):
    date = time.time()
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    db_cursor.execute('INSERT INTO library_map (showtitle, title, showtype, episode, season, filename, shoko_eid, direction, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
     showtitle, title, showtype, episode, season, filename, shoko_eid, direction, date))
    db_connection.commit()
    db_connection.close()


def get_data_from_map(showtitle=None, title=None, showtype=None, episode=None, season=None, filename=None):
    items = None
    try:
        db_connection = database.connect(db_file)
        db_cursor = db_connection.cursor()
        if showtitle is not None and title is not None and showtype is not None and episode is not None and season is not None:
            db_cursor.execute('SELECT showtitle, title, showtype, episode, season, filename, shoko_eid, direction, created FROM library_map WHERE showtitle=? and title=? and showtype=? and episode=? and season=?', (
             showtitle, title, showtype, episode, season))
        else:
            if filename is not None:
                db_cursor.execute('SELECT showtitle, title, showtype, episode, season, filename, shoko_eid, direction, created FROM library_map WHERE filename=?', (
                 filename,))
        items = db_cursor.fetchone()
    except:
        pass

    return items


def remove_map(filename=None, shoko_eid=None):
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    if filename is not None:
        db_cursor.execute('DELETE FROM library_map WHERE filename=?', (filename,))
    else:
        if shoko_eid is not None:
            db_cursor.execute('DELETE FROM library_map WHERE shoko_eid=?', (shoko_eid,))
        else:
            db_cursor.execute('DELETE FROM library_map')
    db_connection.commit()
    db_connection.close()
    return
# okay decompiling library_map.pyo
