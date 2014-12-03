import xbmcplugin
import xbmcgui
import urllib

import util as util

def menu():
    showId = util.pluginArgs['id']
    season = int(util.pluginArgs['season'])
    episodes = util.api.getSeasons(showId, {'season': season})
    episodeNums = episodes.keys()
    episodeNums.sort(key = int)
    thumbnailImage = util.api.getShowPoster(showId)

    for episodeNum in episodeNums:
        episode = episodes[episodeNum]
        
        listItem = xbmcgui.ListItem(
            label = episodeNum + '. ' + episode['status'] + ': ' + episode['name'],
            thumbnailImage = thumbnailImage
        )
        listItem.addContextMenuItems([
            ('Set Episode Status', util.getContextCommand('episodeStatus', [showId, season, episodeNum])),
            ('Set Season Status', util.getContextCommand('seasonStatus', [showId, season])),
            ('Manual Search', util.getContextCommand('episodeSearch', [showId, season, episodeNum])),
            ('Refresh list', util.getContextCommand('refresh'))
        ], True)
        xbmcplugin.addDirectoryItem(
            handle = util.pluginId,
            url = '',
            listitem = listItem,
            isFolder = False
        )

    xbmcplugin.endOfDirectory(util.pluginId)        

