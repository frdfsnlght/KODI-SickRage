import xbmc
import xbmcgui

import util as util

showId = sys.argv[1]
show = util.api.getShow(showId)
dialog = xbmcgui.Dialog()
if dialog.yesno('Delete Show', 'Are you sure you want to delete ' + show['show_name'] + '?'):
    result = util.api.doShowDelete(showId)
    xbmc.executebuiltin('Container.Refresh')
