import resources.lib.util as util

# wrap this in a try/catch to catch broken API calls (can't connect, timeout, etc)

try:
    if 'vf' in util.pluginArgs:
        vf = util.pluginArgs['vf']
        if vf == 'shows':
            import resources.lib.shows as shows
            shows.menu()
        elif vf == 'upcoming':
            import resources.lib.upcoming as upcoming
            upcoming.menu()
        elif vf == 'history':
            import resources.lib.history as history
            history.menu()
        elif vf == 'backlog':
            import resources.lib.backlog as backlog
            backlog.menu()
        elif vf == 'failed':
            import resources.lib.failed as failed
            failed.menu()
        elif vf == 'seasons':
            import resources.lib.seasons as seasons
            seasons.menu()
        elif vf == 'episodes':
            import resources.lib.episodes as episodes
            episodes.menu()
        else:
            util.log('invalid folder "' + vf + '"')
            import resources.lib.main as main
            main.menu()
    elif 'action' in util.pluginArgs:
        action = util.pluginArgs['action']
        if action == 'showAdd':
            import resources.lib.showAdd as showAdd
            showAdd.action()
        else:
            util.log('invalid folder "' + vf + '"')
    else:
        import resources.lib.main as main
        main.menu()

except IOError as ioe:
    util.message('Error', '%s' % ioe)
    
