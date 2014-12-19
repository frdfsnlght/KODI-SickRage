import xbmc
import xbmcgui

from operator import itemgetter

import util as util

def action():
    
    # Get the name
    
    keyboard = xbmc.Keyboard('', 'Search for...', False)
    keyboard.doModal()
    if not keyboard.isConfirmed():
        return
    searchName = keyboard.getText() 

    # Get indexer to use
    
    indexers = ['All Indexers', 'theTVDB', 'TVRage']
    dialog = xbmcgui.Dialog()
    indexerIndex = dialog.select('Indexer to Search', indexers)
    if indexerIndex == -1:
        return
    
    # Do the search
    
    matches = util.api.doSearch(searchName, indexerIndex)
    if not matches:
        util.message('Search Results', 'No matching shows found.')
        return

    matchList = []
    for show in matches:
        if not indexerIndex == 0:
            if not show['indexer'] == indexerIndex:
                continue
            indexer = ''
        else:
            if 'tvdbid' in show:
                indexer = 'theTVDB'
            elif 'tvrageid' in show:
                indexer = 'TVRage'
            else:
                indexer = 'Unknown'
        matchList.append(show['name'] + ' - ' + util.formatDate(show['first_aired']) + ' ' + indexer)
    dialog = xbmcgui.Dialog()
    matchIndex = dialog.select('Search Results', matchList)
    if matchIndex == -1:
        return
    show = matches[matchIndex]

    # Get the parent directory
    
    rootDirs = util.api.getRootDirs()
    if not rootDirs:
        util.message('Error', 'There are no root directories defined!')
        return

    dirs = []
    for rootDir in rootDirs:
        dirs.append(('* ' if rootDir['default'] == 1 else '') + rootDir['location'])
        
    dialog = xbmcgui.Dialog()
    dirIndex = dialog.select('Parent Folder', dirs)
    if dirIndex == -1:
        return
    location = rootDirs[dirIndex]['location']

    # Get show options
    
    defaults = util.api.getDefaults()
    
    # ... initial status
    
    statuses = ['wanted', 'skipped', 'archived', 'ignored']
    statusList = []
    for status in statuses:
        statusList.append(('* ' if status == defaults['status'] else '') + status.title())
    dialog = xbmcgui.Dialog()
    statusIndex = dialog.select('Initial Episode Status', statusList)
    if statusIndex == -1:
        return
    status = statuses[statusIndex]

    # ... flatten folders

    # no way for user to cancel this (looks like No/False)!
    flattenFolders = dialog.yesno('Flatten Folders', 'Flatten season folders?', 'Default: ' + 'Yes' if defaults['flatten_folders'] else 'No')

    # ... anime

    anime = dialog.yesno('Anime', 'Is this show an Anime?')
    
    # ... scene numbering

    sceneNumbered = dialog.yesno('Scene Numbering', 'Is this show scene numbered?')
    
    # ... quality
    
    qualities = [
        'sdtv|sddvd',
        'hdtv|hdwebdl|hdbluray',
        'fullhdtv|fullhdwebdl|fullhdbluray',
        'hdtv|fullhdtv|hdwebdl|fullhdwebdl|hdbluray|fullhdbluray',
        'sdtv|sddvd|hdtv|fullhdtv|hdwebdl|fullhdwebdl|hdbluray|fullhdbluray|unknown'
    ]
    qualityList = [
        'SD',
        'HD720p',
        'HD1080p',
        'HD',
        'Any'
    ]
    defaultQuality = '|'.join(defaults['initial'])
    try:
        qualityList[qualities.index(defaultQuality)] = '* ' + qualityList[qualities.index(defaultQuality)]
    except:
        pass
    dialog = xbmcgui.Dialog()
    qualityIndex = dialog.select('Quality', qualityList)
    if qualityIndex == -1:
        return
    quality = qualities[qualityIndex]
    
    # Add the show!
    
    if 'tvdbid' in show:
        indexerid = show['tvdbid']
        indexer = 'tvdb'
    elif 'tvrageid' in show:
        indexerid = show['tvrageid']
        indexer = 'tvrage'
    else:
        indexerid = None
    result = util.api.doAddNewShow(indexerid, indexer, location, status, flattenFolders, anime, sceneNumbered, quality)
    if result['result'] == 'success':
        util.message('Add Show', 'The show has been added.', 'It may take a moment before it appears in the list.')
        xbmc.executebuiltin('Container.Refresh')
        
