import xbmcplugin
import xbmcgui
import urllib
import re

import util as util

def menu():
    history = util.api.getHistory()
    shows = {}
    
    for show in history:
        uId = str(show['tvdbid']) + '-' + str(show['season']) + '-' + str(show['episode'])
        if (not uId in shows) or (show['status'] == 'Downloaded'):
            shows[uId] = show
                
    shows = shows.values()
    shows.sort(key = lambda show: show['date'], reverse = True)

    for show in shows:
        url = util.getShowURL(show['tvdbid'])
        listItem = xbmcgui.ListItem(
            label = util.formatDateTime(show['date']) + ': ' + show['status'] + ' ' + util.formatEpisodeName(show),
            iconImage = util.getIcon('downloaded' if show['status'] == 'Downloaded' else 'snatched')
            #thumbnailImage = util.api.getShowPosterThumbnail(show['tvdbid'])
        )
        listItem.addContextMenuItems([
            ('Refresh list', util.getContextCommand('refresh'))
        ], True)
        xbmcplugin.addDirectoryItem(
            handle = util.pluginId,
            url = url,
            listitem = listItem,
            isFolder = True
        )

    xbmcplugin.endOfDirectory(util.pluginId)        
