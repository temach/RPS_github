#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import pickle
import pygame
import pygame.locals as PL


from elements import Button, Reader
import util
import small_util



class MakerLocal( util.MakerBasic ):
    pass



class HighScore( util.ModuleBasic ):

    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()


        # specific variables for this cluster
        self.reader = None
        self.scores_file = "high_scores.txt"

        self._objects_scores = {}



    """ Modify default function behaviour """
    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_menu(self, func_vars=None):
        self.cp.unbind( self.map.objects_scores )
        self.cp.unbind( self._objects_scores )

    def func_show_winner(self, func_vars=None):
        self.cp.unbind( self.map.objects_scores )
        self.cp.unbind( self._objects_scores )


    def func_view_scores(self, func_vars=None):

        # PlayerName : { OpponentName1:NumberOfWins,  OpponentName2:NumberOfWins }
        scores = small_util.read_pickle_file( self.scores_file ) or {}

        if func_vars["view_from"]=="display_winner":
            self.cp.bind( self._objects_scores )

        text = """   Name _>   Opponent's Name : Number of wins"""

        try:
            for p_name, o_info in scores.items():
                text += "\n\n\t {0} has beaten".format( p_name )
                for o_name, o_wins in o_info.items():
                    text += "\n\t\t\t {0} : {1}   times".format( o_name, str(o_wins))
        except ValueError:
            pass    # the scores file is empty


        self.reader.update_text( text )     # this is using the handle to the reader object created by the self.setup() function
        self.cp.bind( self.map.objects_scores )
    """ End modify section """


    #def _func_exit(self, func_vars=None):




    """ Modify default object existence """
    def setup(self):
        self.ops.func_view_scores.append( self.func_view_scores )
        self.ops.func_show_winner.append( self.func_show_winner )
        self.ops.func_main_menu.append( self.func_menu )

        # things that exist within the space
        rect = pygame.Rect( (40,460), (100,90))
        img = "menu"
        b = self.maker.make_button( rect, self.ops.func_main_menu, img, func_vars=None, rescale=True)
        self.map.objects_scores["exit_to_menu"] = b

        rect = pygame.Rect( (400,460), (100,90))
        img = "next"
        b = self.maker.make_button( rect, self.ops.func_show_winner, img, func_vars=None, rescale=True)
        self._objects_scores["exit_to_winner"] = b


        text = ""
        r = self.maker.make_reader( text, (94, 58), 615, "style_reader2")
        self.map.objects_scores["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)



    def debug_setup(self):
        """Use this to define the infrastructure that will be needed for the
        module to function. In other words define the objects which affect
        the module's initial entering and/or exiting conditions. Things that
        surround this module, but are also implemented elsewhere. Call this function
        when you want to test one module in isolation.
        """

        rect = pygame.Rect( (80,180), (160,60))
        img = "scores"
        b = self.maker.make_button(rect, self.ops.func_view_scores, img, func_vars={"view_from":"menu"}, rescale=True)
        self.map.objects_menu["func_view_scores"] = b

