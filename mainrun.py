#! /usr/bin/env python-32
# -*- coding: utf-8 -*-





"""
Resolve Clash of Titans
"""


import pygame
import pygame.locals as PL
import time
from sys import exit


# Start utilities imports (my)
import constants        # Later this should combine, game constants AND pygame.locals constants
import resources

from util import debug      # Use as decorator. So put "@debug" just before function definition.
from util import ActiveGroup, FunctionsGroup
# End my utilities imports

# Start my modules imports
from m_mainmenu import MainMenuModule
from m_splash
from m_scores


class Operator(object):     # The operator describes what functions there are, in your files you describe how they work.
    def __init__(self):
        self.func_main_menu = FunctionsGroup()
        self.func_game = FunctionsGroup()
        self.func_view_scores = FunctionsGroup()
        self.func_credits = FunctionsGroup()


class Mapper(object):      # Describes what options you have. In your files you describe how these dictionaries look, the Mapper describes what dictionaries there are.
    def __init__(self):
        self.objects_menu = {}




pygame.init()


"Setup"
screen = pygame.display.set_mode( (800,600) )

# icon = pygame.transform.scale( resources.get_image("icon"), (32, 32))
#pygame.display.set_icon(icon)
#pygame.display.set_caption('Pygame Aliens')

background = pygame.Surface( screen.get_size() )
background.fill( (240,240,240) )

screen.blit( background, (0,0))
pygame.display.flip()
"End"



clock = pygame.time.Clock()

operators = Operator()
mapper = Mapper()
active = ActiveGroup()


# Here we enter the names of the modules
module = MainMenuModule( active, operators, mapper )
module.setup()


active.bind( mapper.objects_menu )





legal_events = (PL.KEYDOWN, PL.KEYUP, PL.MOUSEMOTION, PL.MOUSEBUTTONUP, PL.MOUSEBUTTONDOWN)
keyboard_events =(PL.KEYDOWN, PL.KEYUP)


while True:
    event = pygame.event.wait()

    if event.type==PL.QUIT or ( (event.type in keyboard_events) and (event.key == PL.K_q or event.key==PL.K_ESCAPE) ):
        exit()

    elif event.type in legal_events:
        active.manage_event( event )

    active.clear(screen, background)

    dirty_rects = active.manage_render( screen )
    pygame.display.update(dirty_rects)

    active.manage_run()

    clock.tick(20)








