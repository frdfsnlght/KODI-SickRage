import xbmc
import xbmcgui

import util as util

showId = util.pluginArgs[0]
season = util.pluginArgs[1]

statuses = ['wanted', 'skipped', 'archived', 'ignored', 'failed']
statusList = []
for status in statuses:
    statusList.append(status.title())
dialog = xbmcgui.Dialog()
statusIndex = dialog.select('Season Status', statusList)
if not statusIndex == -1:
    status = statuses[statusIndex]
    result = util.api.doEpisodeSetStatus(showId, season, None, status)
    if result['result'] == 'success':
        xbmc.executebuiltin('Container.Refresh')

