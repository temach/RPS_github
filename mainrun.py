#! /usr/bin/env python-32
# -*- coding: utf-8 -*-


"""
Resolve Clash of Titans
"""


import pygame
import pygame.locals as PL
import time
from sys import exit


#start my util imports
import constants            # Later this should combine, game constants AND pygame.locals constants
import resources

from util import ActiveGroup

from small_util import debug              # Use as decorator. So put "@debug" just before function definition.
from small_util import FunctionsGroup
#end


#start my modules
import m_mainmenu
import m_splash
import m_scores
import m_pickname


class Operator(object):     # The operator describes what functions there are, in your files you describe how they work.
    def __init__(self):
        self.func_main_menu = FunctionsGroup()
        self.func_game = FunctionsGroup()
        self.func_view_scores = FunctionsGroup()
        self.func_credits = FunctionsGroup()
        self.func_splash_screen = FunctionsGroup()

        #self.func_submit_name = FunctionsGroup()
        #self.func_pick_name = FunctionsGroup()     Suggestion: replace self.func_game with this

        #self.func_submit_weapon = FunctionsGroup()
        self.func_pick_weapon = FunctionsGroup()




class Mapper(object):      # Describes what options you have. In your files you describe how these dictionaries look, the Mapper describes what dictionaries there are.
    def __init__(self):
        self.objects_menu = {}
        self.objects_splash_screen = {}     # the first thing to be bind'ed
        self.objects_scores = {}
        self.objects_pick_name = {}



pygame.init()


#setup
screen = pygame.display.set_mode( (800,600) )

#icon = pygame.transform.scale( resources.get_image("icon"), (32, 32))
#pygame.display.set_icon(icon)
pygame.display.set_caption('Rock : Paper : Scissors')

background = pygame.Surface( screen.get_size() )
background.fill( (240,240,240) )

screen.blit( background, (0,0))
pygame.display.flip()
#end



clock = pygame.time.Clock()

operators = Operator()
mapper = Mapper()
active = ActiveGroup()


# Here we enter the names of the modules
module1 = m_mainmenu.MainMenuModule( active, operators, mapper )
module1.setup()

module2 = m_splash.SplashModule( active, operators, mapper )
module2.setup()

module3 = m_scores.HighScore( active, operators, mapper )
module3.setup()

module4 = m_pickname.PickName( active, operators, mapper )
module4.setup()



#active.bind( mapper.objects_menu )
operators.func_game()


legal_events = (PL.KEYDOWN, PL.KEYUP, PL.MOUSEMOTION, PL.MOUSEBUTTONUP, PL.MOUSEBUTTONDOWN)
keyboard_events =(PL.KEYDOWN, PL.KEYUP)


while True:
    event_que = pygame.event.get()

    for event in event_que:
        if event.type==PL.QUIT or ( (event.type in keyboard_events) and (event.key == PL.K_q or event.key==PL.K_ESCAPE) ):
            exit()

        elif event.type in legal_events:
            active.manage_event( event )

    active.clear(screen, background)

    dirty_rects = active.manage_render( screen )
    pygame.display.update(dirty_rects)

    active.manage_run()

    clock.tick(40)








