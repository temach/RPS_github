# first one below is a preset
style_button_menu = dict( size=(70,70) )

style_button_game = dict(
    img="start_game",
    **style_button_menu )

style_button_scores = dict(
    img="scores",
    **style_button_menu  )

style_button_next = dict(
    img="next_round",       # next round
    size=(94,47)  )

style_button_restart = dict(
    img="restart",      # restart current round, so let player1 choose weapon again
    **style_button_menu  )

style_button_info = dict(
    img="info",
    **style_button_menu  )

style_button_menu = dict(
    img="menu",
    **style_button_menu  )

style_button_next = dict(           # start next round from the view winner screen
    img="next",
    **style_button_menu  )


# first one below is a preset
style_button_weapon = dict( size=(140,70) )

style_button_rock = dict(
    img="rock",
    **style_button_weapon )

style_button_paper = dict(
    img="paper",
    **style_button_weapon )

style_button_scissors = dict(
    img="scissors",
    **style_button_weapon )

style_button_confirm = dict(
    size = (20,20),
    img = "confirm",
)


style_form1 = dict(                 # tiny single line input
    fontsize = 12,
    height = 20,
    font = "mono",
    bgcolor = (100,100,100),
    fgcolor = (250,250,250),       # text color
    hlcolor = (250,190,150,50),    # highlighted text color
    curscolor = (190,0,10),
    maxlines = 1,                  # wrap lines automatically
)

style_form2 = dict(             # large single line input
    fontsize = 25,
    height = 30,
    font = "mono",
    bgcolor = (100,100,100),
    fgcolor = (250,250,250),       # text color
    hlcolor = (250,190,150,50),    # highlighted text color
    curscolor = (190,0,10),
    maxlines = 1,                  # wrap lines automatically
)


style_reader1 = dict(           # small reader, small height
    fontsize = 17,
    font = "mono",
    height = 100,
    bgcolor = (240,240,240,0),
    fgcolor = (150,150,150,0),           # text color
    hlcolor = (180,180,200,0),      # highlighted text color
    split = True,                  # wrap lines automatically
)

style_reader2 = dict(           # small reader, big height
    fontsize = 17,
    font = "mono",
    height = 300,
    bgcolor = (150,150,150,0),
    fgcolor = (0,0,0,0),           # text color
    hlcolor = (180,180,200,0),      # highlighted text color
    split = True,                  # wrap lines automatically
)
