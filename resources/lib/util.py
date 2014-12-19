import xbmcplugin
import xbmcgui
import xbmcaddon
import urllib
import urlparse
import pprint
import sys
import os

plugin = xbmcaddon.Addon(id = 'plugin.program.sickrage')

import sickrage

def log(obj):
    if not isinstance(obj, basestring):
        msg = pprint.pformat(obj)
    else:
        msg = str(obj)
    print 'Sickrage plugin: ' + msg

def getShowURL(id):    
    return pluginURL + '?' + urllib.urlencode({
        'vf': 'seasons',
        'id': id
    })
    
def getContextCommand(cmd, args = []):
    cmd = 'XBMC.RunScript(special://home/addons/plugin.program.sickrage/resources/lib/' + cmd + '.py'
    if args:
        args = [str(i) for i in args]
        cmd = cmd + ', ' + ', '.join(args)
    cmd = cmd + ')'
    return cmd

def getIcon(name):
    return os.path.join(iconDir, name + '.png')
    
def getFolderURL(vf):
    params = {'vf': vf}
    url = pluginURL + '?' + urllib.urlencode(params)
    return url

def getActionURL(action, params = {}):
    params['action'] = action
    url = pluginURL + '?' + urllib.urlencode(params)
    return url
    
def getKWArguments(argv):
    if not argv:
        return {}
    if argv.startswith('?'):
        argv = argv[1:]
    #log('argv is now ' + argv)
    args = urlparse.parse_qs(argv)
    #log(args)
    newArgs = {}
    for key, val in args.iteritems():
        #log('key=' + key)
        if len(val) == 1:
            newArgs[key] = val[0]
        else:
            newArgs[key] = val
    return newArgs

def message(header, line1, line2 = None, line3 = None):
    dialog = xbmcgui.Dialog()
    dialog.ok(header, line1, line2, line3)

def formatDate(date):
    # assumes YYYY-MM-DD
    date = date.split('-')
    fmt = plugin.getSetting('dateFormat')
    if fmt == 'M/D/Y':
        return date[1] + '/' + date[2] + '/' + date[0]
    elif fmt == 'D/M/Y':
        return date[2] + '/' + date[1] + '/' + date[0]
    else:
        return '?'

def formatTime(time, ampm = None):
    # assumes 'HH:MM' or 'HH:MM', 'AM'
    time = time.split(':')
    time[0] = int(time[0])
    if not ampm:
        if time[0] > 12:
            ampm = 'PM'
            time[0] = time[0] - 12
        else:
            ampm = 'AM'
            if time[0] == 0:
                time[0] = 12
    time[0] = str(time[0])
    fmt = plugin.getSetting('timeFormat')
    if fmt == 'AM/PM':
        return time[0] + ':' + time[1] + ' ' + ampm
    elif fmt == '24 Hour':
        return str(int(time[0]) + 12) + ':' + time[1]
    else:
        return '?'
        
def formatDateTime(dateTime):
    # assumes YYYY-MM-DD HH:MM
    dateTime = dateTime.split(' ')
    date = formatDate(dateTime[0])
    time = formatTime(dateTime[1])
    return date + ', ' + time

def formatEpisodeName(show):
    out = show['show_name'] + ' - ' + str(show['season']) + 'x' + ('%02d' % show['episode'])
    if 'ep_name' in show:
        out = out + ' - ' + show['ep_name']
    return out

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

pluginURL = sys.argv[0]
if pluginURL.endswith('.py'):
    pluginId = None
    pluginArgs = sys.argv[1:]
else:
    pluginId = int(sys.argv[1])
    pluginArgs = getKWArguments(sys.argv[2])
    
api = sickrage.API()
iconDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons')

log(sys.argv)
#log('iconDir: ' + iconDir)
#log('pluginURL: ' + pluginURL)
#log('pluginId: ' + str(pluginId))
log(pluginArgs)