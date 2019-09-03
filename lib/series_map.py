# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import xbmcaddon
import xbmc
import os
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
    db_file = os.path.join(profileDir, 'a_map.db')
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute('CREATE TABLE IF NOT EXISTS [library_map] ([tid] INTEGER NOT NULL, [aid] INTEGER NOT NULL, [sid] INTEGER NOT NULL);')
    except:
        pass

db_connection.close()


def add_map(tid, aid, sid):
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    db_cursor.execute('INSERT INTO library_map (tid, aid, sid) VALUES (?, ?, ?)', (tid, aid, sid))
    db_connection.commit()
    db_connection.close()


def get(tid=0, aid=0, sid=0):
    items = None
    try:
        db_connection = database.connect(db_file)
        db_cursor = db_connection.cursor()
        if tid != 0 and aid == 0 and sid == 0:
            db_cursor.execute('SELECT tid, aid, sid FROM library_map WHERE tid=?', (tid,))
        elif tid == 0 and aid != 0 and sid == 0:
            db_cursor.execute('SELECT tid, aid, sid FROM library_map WHERE aid=?', (aid,))
        elif tid == 0 and aid == 0 and sid != 0:
            db_cursor.execute('SELECT tid, aid, sid FROM library_map WHERE sid=?', (sid,))
        items = db_cursor.fetchone()
    except:
        pass
    return items


def get_all():
    items = None
    try:
        db_connection = database.connect(db_file)
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT tid, aid, sid FROM library_map')
        items = db_cursor.fetchall()
    except:
        pass
    return items


def check(tid=0, aid=0, sid=0):
    try:
        db_connection = database.connect(db_file)
        db_cursor = db_connection.cursor()
        if tid != 0 and aid != 0 and sid != 0:
            db_cursor.execute('SELECT tid, aid, sid FROM library_map WHERE tid=? and aid=? and sid=?', (tid, aid, sid))
            items = db_cursor.fetchone()
            if len(items) > 0:
                return True
    except:
        return False
    return False


def remove_map(tid=0, aid=0, sid=0):
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    if tid != 0 and aid == 0 and sid == 0:
        db_cursor.execute('DELETE FROM library_map WHERE tid=?', (tid,))
    elif tid == 0 and aid != 0 and sid == 0:
        db_cursor.execute('DELETE FROM library_map WHERE aid=?', (aid,))
    elif tid == 0 and aid == 0 and sid != 0:
        db_cursor.execute('DELETE FROM library_map WHERE sid=?', (sid,))
    else:
        db_cursor.execute('DELETE FROM library_map')
    db_connection.commit()
    db_connection.close()
    return

