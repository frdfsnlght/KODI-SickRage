import xbmcplugin
import xbmcgui

import resources.lib.util as util

def menu():
    util.xbmcAddDirectory('Shows', 'shows')
    util.xbmcAddDirectory('Upcoming', 'upcoming')
    util.xbmcAddDirectory('History', 'history')
    util.xbmcAddDirectory('Backlog', 'backlog')
    util.xbmcAddDirectory('Failed Downloads', 'failed')
    util.xbmcEndDirectory()        
