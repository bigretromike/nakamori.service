#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xbmc

__scriptname__ = "nakamori.service"


def log(msg):
    xbmc.log("nakamori.service::%s" % msg, level=xbmc.LOGDEBUG)


if __name__ == '__main__':
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            log("exiting")
            break
