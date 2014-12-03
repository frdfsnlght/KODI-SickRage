import xbmcplugin
import xbmcgui
import urllib
import re

import util as util

def menu():
    shows = util.api.getBacklog()
    shows.sort(key = lambda show: re.sub(r'^(?i)(the)\s+', '', show['show_name']))
    
    for show in shows:
        url = util.getShowURL(show['indexerid'])
        for ep in show['episodes']:
            ep['show_name'] = show['show_name']
            listItem = xbmcgui.ListItem(
                label = util.formatEpisodeName(ep),
                iconImage = util.getIcon('wanted' if ep['status'] == 3 else 'qual')
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

