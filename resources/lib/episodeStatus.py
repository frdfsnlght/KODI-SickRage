import xbmc
import xbmcgui

import util as util

showId = util.pluginArgs[0]
season = util.pluginArgs[1]
episode = util.pluginArgs[2]
currentStatus = util.pluginArgs[3].lower()

statuses = ['wanted', 'skipped', 'archived', 'ignored', 'failed']
statusList = []
for status in statuses:
    statusList.append(('* ' if status == currentStatus else '') + status.title())
dialog = xbmcgui.Dialog()
statusIndex = dialog.select('Episode Status', statusList)
if not statusIndex == -1:
    status = statuses[statusIndex]
    if not status == currentStatus:
        result = util.api.doEpisodeSetStatus(showId, season, episode, status)
        if result['result'] == 'success':
            xbmc.executebuiltin('Container.Refresh')

