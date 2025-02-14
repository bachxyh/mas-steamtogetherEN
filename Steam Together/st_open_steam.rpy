init 5 python:
    import os
    import io

    def get_steam_library_paths(steam_path):
        """Returns the paths of the Steam libraries"""
        library_folders_path = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
        library_paths = []
        
        if os.path.exists(library_folders_path):
            with open(library_folders_path, 'r') as file:
                library_folders = file.read()
            
            for line in library_folders.splitlines():
                if 'path' in line:
                    path = line.split('"')[3]
                    library_paths.append(path)
        
        return library_paths

    def get_installed_games(steam_path):
        """Returns a list of installed games on Steam"""
        installed_games = []
        library_paths = get_steam_library_paths(steam_path)
        
        for library_path in library_paths:
            steamapps_path = os.path.join(library_path, 'steamapps')
            if os.path.exists(steamapps_path):
                for file in os.listdir(steamapps_path):
                    if file.endswith('.acf'):
                        game_info_path = os.path.join(steamapps_path, file)
                        with open(game_info_path, 'r') as game_file:
                            game_info = game_file.read()
                            if '"name"' in game_info:
                                game_name = game_info.split('"name"')[1].split('"')[1]
                                installed_games.append(game_name)
        
        return installed_games

    steam_path = "C:\\Program Files (x86)\\Steam"
    installed_games = get_installed_games(steam_path)

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="st_openyour_steam",  
            category=['steam'],
            prompt="Could you open Steam for me?",
            random=False,
            pool=True,
            unlocked=True,
        )
    )

screen mas_game_menu():
    modal True
    zorder 200

    frame:
        style_prefix "choice"
        xpos 980
        ypos 100
        xsize 300
        ysize 500
        background None

        has vbox
        spacing 10
        text "{i}Installed Games{/i}" size 40 xalign 0.5

        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            ysize 400

            has vbox
            spacing 5
            for game in installed_games:
                textbutton game:
                    action Return(game)
                    style "choice_button"
                    xfill True
            textbutton "Forget it":
                action Return("cancel")
                style "choice_button"
                xfill True

label st_openyour_steam:
    $ steam_exe_path = "C:\\Program Files (x86)\\Steam\\Steam.exe"

    if os.path.exists(steam_exe_path):
        m 1eud "Oh, you want to open Steam, [player]?"
        m 1eub "Just give me a second..."
        m 1dua "..."
        $ os.startfile(steam_exe_path)
        m 3hub "All set! Steam is open!"

        m 3eub "Now, tell me: what are you going to play today?"
        call screen mas_game_menu  
        $ selected_game = _return

        if selected_game and selected_game != "cancel":
            m 3wub "Great choice! [selected_game] looks like a lot of fun!"
            
            m 3hub "Are you going to play now or later?{nw}"
            $ _history_list.pop()
            menu:
                "I'm playing now.":
                    m 3wub "Got it! Enjoy the game a lot, [player]!"
                    m 3rksdlb "But don't forget to come back and spend some time with me later, okay?"
                    m 1tublb "I might get jealous if you spend too much time on another game without me."
                    m 1hub "If you need a break, I'll be here waiting for you!"
                    m 3fubsb "Anyway, I hope you have a lot of fun!"
                    $ mas_idle_mailbox.send_idle_cb("st_openyour_steam_callback")
                    return "idle"

                "I'll play later.":
                    m 1eua "Oh, that's fine!"
                    m 3hub "If you change your mind, just let me know."
                    return

        elif selected_game == "cancel":
            m 1eud "Oh, you decided not to choose a game?"
            m 2sub "That's okay! Sometimes it's nice to just browse."
            m 3hub "If you want to play something later, just let me know!"
            return

    else:
        m 2wud "Hmm, I can't seem to find Steam on your computer..."
        m 1tku "Are you sure it's installed?"
        m 5hub "If you need help, I can try again later!"
    
    return

label st_openyour_steam_callback:
    $ import datetime
    
    if persistent.last_game_time:
        $ last_time = datetime.datetime.fromisoformat(persistent.last_game_time)
        $ now = datetime.datetime.now()
        $ time_diff = (now - last_time).total_seconds()
    else:
        $ time_diff = 0

    if time_diff < 300:
        m 3wub "Oh, you came back very quickly!"
        m 1ttb "Changed your mind or were you doing a speedrun?~"

        $ _history_list.pop()
        menu:
            "I'm just taking a break.":
                m 3hub "Got it!"
                m 5ekb "Breaks are important! I don't want you to get too tired staring at the screen."
                m 7ekb "When you're ready to go back to playing, let me know, okay?"

            "Yes, I'm done!":
                m 1wub "Really?"
                m 2sub "So, how was it? Did you have fun?"
                m 2tku "I hope it was enjoyable, but not so much that you forget about me~"

    elif time_diff < 1800:
        m 1wub "Oh, you're back!"
        m 7eub "Did you finish playing, [player]?"

        $ _history_list.pop()
        menu:
            "I'm just taking a break.":
                m 3hub "Got it!"
                m 5ekb "Breaks are important! I don't want you to get too tired staring at the screen."
                m 7ekb "When you're ready to go back to playing, let me know, okay?"

            "Yes, I'm done!":
                m 1wub "Really?"
                m 2sub "So, how was it? Did you have fun?"
                m 2tku "I hope it was enjoyable, but not so much that you forget about me~"

    else:
        m 7wud "Wow, you played for such a long time?"
        m 2ttb "Was the game that good, or did you forget about me?~"
        m 1eua "Haha~ I'm just teasing you."
        m 5fkb "The important thing is that you enjoyed it."

    return
