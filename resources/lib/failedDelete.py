import xbmc
import xbmcgui

import util as util

dialog = xbmcgui.Dialog()
if dialog.yesno('Delete Failed Download', 'Delete this failed download?'):
    # need API for failed deletion
    release = util.pluginArgs[0]
    util.log('TODO: delete ' + release)
    #result = util.api.doDeleteFailed(release)
    #if result['result'] == 'success':
        #xbmc.executebuiltin('Container.Refresh')

