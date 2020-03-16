# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import xbmcaddon
import xbmc
import os
from error_handler import spam, log  # lib

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
    db_file = os.path.join(profileDir, 's_map.db')
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute('CREATE TABLE IF NOT EXISTS [sync_date] ([date] TEXT NOT NULL);')
    except:
        pass
    try:
        db_cursor.execute('CREATE TABLE IF NOT EXISTS [queue] ([aid] INTEGER NOT NULL, [eid] INTEGER NOT NULL, [sid] INTEGER NOT NULL, [rating] INTEGER NOT NULL);')
    except:
        pass
    db_connection.close()


def add_to_queue(aid, eid, sid, rating=0):
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT aid, eid, sid FROM queue WHERE aid=? and eid=? and sid=?', (aid, eid, sid))
    if db_cursor.fetchone() is None:
        db_cursor.execute('INSERT INTO queue (aid, eid, sid, rating) VALUES (?, ?, ?, ?)', (aid, eid, sid, rating))
        db_connection.commit()
        db_connection.close()
        spam(' ===> add_to_queue: added')
    spam(' ===> add_to_queue: %s %s %s' % (aid, eid, sid))


def add_date(date):
    db_connection = database.connect(db_file)
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT date FROM sync_date WHERE date=?', (date,))
    if db_cursor.fetchone() is None:
        db_cursor.execute('INSERT INTO sync_date (date) VALUES (?)', (date,))
        db_connection.commit()
        db_connection.close()
        spam(' ===> add_date: %s: True' % (date,))
        return True
    spam(' ===> add_date: %s: False' % (date,))
    return False


def get_queue():
    items = None
    try:
        db_connection = database.connect(db_file)
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT aid, eid, sid, rating FROM queue')
        items = db_cursor.fetchall()
    except:
        pass
    spam(' ===> get_queue: %s' % (len(items),))
    return items


def get_lastdate():
    items = None
    try:
        db_connection = database.connect(db_file)
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT date FROM sync_date ORDER BY date DESC')
        items = db_cursor.fetchone()
        if items is None:
            items = ['2000-01-01']
    except:
        pass
    spam(' ===> get_latestdate: %s' % (items,))
    return items


def clear_queue(number_of_items=0):
    # as a safe-lock, check number of items before flushing, if its same then flush,
    # if different then something was added and it would be better to process it again
    if len(get_queue()) == number_of_items:
        db_connection = database.connect(db_file)
        db_cursor = db_connection.cursor()
        db_cursor.execute('DELETE FROM queue')
        db_connection.commit()
        db_connection.close()
        spam(' ===> clear_queue: True')
        return True
    spam(' ===> clear_queue: False')
    return False
