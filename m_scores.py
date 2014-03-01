#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import pickle
import pygame
from pygame.locals import *
pygame.init()



from elements import Button, Reader
import util
from util import MakerBasic




def get_filled(surf, col):
    s = surf.copy()
    s.fill( col )
    return s



class MakerLocal( MakerBasic ):

    def make_reader1(self, text, pos, width,
                            fontsize=15,
                            height=None,
                            font=None,
                            bg=(100,100,100),
                            fgcolor=(255,255,255),
                            hlcolor=(255,10,150,100),
                            split=False):
        """ pos and width are necessary. """
        if not type(text)==unicode:
            text = unicode(text.expandtabs(4),'utf8')
        t = Reader( text, pos, width, fontsize, height, font, bg, fgcolor, hlcolor, split)
        return t











class HighScore(object):
    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()


        # specific variables for this cluster
        self.reader = None

        # PlayerName : { OpponentName:NumberOfWins,  OpponentName:NumberOfWins }
        self.scores = util.read_pickle_file( "high_scores.txt" )


        self.objects_scores = {}
        self.objects_menu = {}



    """ Modify default function behaviour """
    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_menu(self, func_vars=None):
        self.cp.unbind( self.objects_scores )


    # What are some of the things that will happen when someone calls "func_view_scores"
    def func_view_scores(self, func_vars=None):
        print
        print "unbinding objects_menu, ", self.objects_menu
        self.cp.unbind(self.objects_menu)
        text = """   Name _>   Opponent's Name : Number of wins"""

        for p_name, o_info in self.scores.items():
            text += "\n\n\t {0} has beaten".format( p_name )
            for o_name, o_wins in o_info.items():
                text += "\n\t\t\t {0} : {1}   times".format( o_name, str(o_wins))


        self.reader.update_text( text )     # this is using the handle to the reader object created by the self.setup() function
        #print
        print "just before bind in func_view_score"
        #print self.objects_scores
        self.cp.bind( self.objects_scores )
        print "ended bind in func_view_score"
    """ End modify section """




    """ Modify default object existence """
    def setup(self):
        self.ops.func_view_scores.append( self.func_view_scores )
        self.ops.func_main_menu.append( self.func_menu )

        # things that exist within the space
        rect = pygame.Rect( (40,460), (100,90))
        img = "menu"
        b = self.maker.make_button( rect, self.ops.func_main_menu, img, func_vars=None, rescale=True)
        self.objects_scores["func_main_menu"] = b


        text = ""
        r = self.maker.make_reader( text, (94, 58), 615, "normallllllllllllllll")
        self.objects_scores["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)


        rect = pygame.Rect( (80,180), (160,60))
        img = "scores"
        b = self.maker.make_button(rect, self.ops.func_view_scores, img, func_vars={"view_from":"menu"}, rescale=True)
        self.objects_menu["func_view_scores"] = b





if __name__=="__main__":

    import pygame
    import pygame.locals as PL
    import time
    from sys import exit

    from util import debug      # Use as decorator. So put "@debug" just before function definition.
    from util import ActiveGroup
    from util import FunctionsGroup


    class Operator(object):     # The operator describes what functions there are, in your files you describe how they work.
        def __init__(self):
            self.func_main_menu = FunctionsGroup()
            self.func_view_scores = FunctionsGroup()


    class Mapper(object):      # Describes what options you have. In your files you describe how these dictionaries look, the Mapper describes what dictionaries there are.
        def __init__(self):
            self.objects_menu = {}
            self.objects_scores = {}


    pygame.init()

    screen = pygame.display.set_mode( (800,600) )


    operators = Operator()
    mapper = Mapper()
    active = ActiveGroup()

    clock = pygame.time.Clock()


    # Here enter the name of the module
    module = HighScore( active, operators, mapper )
    module.setup()

    active.bind( module.objects_menu )


    background = pygame.Surface( screen.get_size() )
    background.fill( (240,240,240) )

    screen.blit( background, (0,0))
    pygame.display.flip()


    legal_events = (PL.KEYDOWN, PL.KEYUP, PL.MOUSEMOTION, PL.MOUSEBUTTONUP, PL.MOUSEBUTTONDOWN)
    keyboard_events =(PL.KEYDOWN, PL.KEYUP)


    while True:
        #screen.blit( background, (0,0))
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
