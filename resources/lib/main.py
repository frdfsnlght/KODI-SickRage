import xbmcplugin
import xbmcgui
import urllib

import resources.lib.util as util

def menu():
    
    def addDirectory(label, vf, params = {}):
        params['vf'] = vf
        url = util.pluginURL + '?' + urllib.urlencode(params)
        listItem = xbmcgui.ListItem(label)
        xbmcplugin.addDirectoryItem(
            handle = util.pluginId,
            url = url,
            listitem = listItem,
            isFolder = True
        )

    addDirectory('Shows', 'shows')
    addDirectory('Upcoming', 'upcoming')
    addDirectory('History', 'history')
    addDirectory('Backlog', 'backlog')
    addDirectory('Failed Downloads', 'failed')
    xbmcplugin.endOfDirectory(util.pluginId)        

