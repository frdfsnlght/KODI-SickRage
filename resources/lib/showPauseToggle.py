import xbmc

import util as util

showId = sys.argv[1]
show = util.api.getShow(showId)
util.api.setShowPause(showId, show['paused'] == 0)
xbmc.executebuiltin('Container.Refresh')