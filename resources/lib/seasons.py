import xbmcplugin
import xbmcgui
import urllib

import util as util

def menu():
    showId = util.pluginArgs['id']
    seasons = util.api.getSeasonList(showId)
    seasons.sort()
    thumbnailImage = util.api.getShowPoster(showId)

    for season in seasons:
        url = util.pluginURL + '?' + urllib.urlencode({
            'vf': 'episodes',
            'id': showId,
            'season': season
        })
        listItem = xbmcgui.ListItem(
            label = ('Season ' + str(season)) if season > 0 else 'Extras',
            thumbnailImage = thumbnailImage
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

