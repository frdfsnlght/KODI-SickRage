import xbmcplugin
import xbmcgui
import urllib
import re

import util as util

def menu():
    shows = util.api.getFuture()
    
    for show in sorted(shows['today'], cmp = compareAirDate):
        addShow(0, show)
    for show in sorted(shows['soon'], cmp = compareAirDate):
        addShow(1, show)
    for show in sorted(shows['later'], cmp = compareAirDate):
        addShow(2, show)

    xbmcplugin.endOfDirectory(util.pluginId)

def addShow(when, show):
    airs = show['airs'].split(' ')
    if when == 0:
        label = util.formatTime(airs[1], airs[2])
        icon = util.getIcon('today');
    elif when == 1:
        label = airs[0] + ' ' + util.formatTime(airs[1], airs[2])
        icon = util.getIcon('soon');
    elif when == 2:
        label = util.formatDate(show['airdate']) + ', ' + airs[0] + ' ' + util.formatTime(airs[1], airs[2])
        icon = util.getIcon('later');
    else:
        icon = None
        
    url = util.getShowURL(show['tvdbid'])
    listItem = xbmcgui.ListItem(
        label = label + ': ' + util.formatEpisodeName(show),
        iconImage = icon
        #thumbnailImage = util.api.getShowPoster(show['tvdbid'])
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

def compareAirDate(showA, showB):
    # compare date
    if showA['airdate'] < showB['airdate']:
        return -1
    elif showA['airdate'] > showB['airdate']:
        return 1
    else:
        # compare AM/PM
        airsA = showA['airs'].split(' ')
        airsB = showB['airs'].split(' ')
        if airsA[2] < airsB[2]:
            return -1
        elif airsA[2] > airsB[2]:
            return 1
        else:
            # compare time
            airsA[1] = airsA[1].rjust(5)
            airsB[1] = airsB[1].rjust(5)
            if airsA[1] < airsB[1]:
                return -1
            elif airsA[1] > airsB[1]:
                return 1
            else:
                return 0
            
            