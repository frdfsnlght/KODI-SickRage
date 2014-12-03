import xbmcplugin
import xbmcgui
import urllib
import re

import util as util

def menu():
    shows = util.api.getShows().values()
    shows.sort(key = lambda show: re.sub(r'^(?i)(the)\s+', '', show['show_name']))

    url = util.getActionURL('showAdd')
    listItem = xbmcgui.ListItem(
        label = 'Add show...',
        thumbnailImage = util.getIcon('showAdd')
    )
    xbmcplugin.addDirectoryItem(
        handle = util.pluginId,
        url = url,
        listitem = listItem,
        isFolder = False
    )
    
    for show in shows:
        url = util.getShowURL(show['tvdbid'])
        listItem = xbmcgui.ListItem(
            label = show['show_name'] + (' (Ended)' if show['status'] == 'Ended' else ''),
            thumbnailImage = util.api.getShowPoster(show['tvdbid'])
        )
        listItem.addContextMenuItems([
            ('Delete show', util.getContextCommand('showDelete', [show['tvdbid']])),
            (('Unpause' if show['paused'] else 'Pause') + ' show', util.getContextCommand('showPauseToggle', [show['tvdbid']])),
            ('Force search', util.getContextCommand('showsSearch')),
            ('Refresh list', util.getContextCommand('refresh'))
        ], True)
        xbmcplugin.addDirectoryItem(
            handle = util.pluginId,
            url = url,
            listitem = listItem,
            isFolder = True
        )

    xbmcplugin.endOfDirectory(util.pluginId)        
