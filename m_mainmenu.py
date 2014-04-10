#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import pygame
import pygame.locals as PL
import sys

from elements import Button
import util

class MakerLocal( util.MakerBasic ):
    pass




class MainMenuModule( util.ModuleBasic ):
    def __init__(self, active, operators, mapper):
        self.active = active
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()



    # Go to scores, exiting function
    def func_view_scores(self, func_vars=None):
        self.active.unbind( self.map.objects_menu )

    # Go to game, exiting function
    def func_game(self, func_vars=None):
        self.active.unbind( self.map.objects_menu )

    # Go to game info, exiting function
    def func_info(self, func_vars=None):
        self.active.unbind( self.map.objects_menu )


    # This is an entry function
    def func_main_menu(self, func_vars=None):
        self.active.bind( self.map.objects_menu )


    def setup(self):
        self.ops.func_info.append( self.func_info )
        self.ops.func_view_scores.append( self.func_view_scores )
        self.ops.func_main_menu.append( self.func_main_menu )
        self.ops.func_game.append( self.func_game )

        # create toys/things for the space
        b = self.maker.make_button( (80,80), "style_button_game", self.ops.func_game, func_vars=None )
        self.map.objects_menu["func_game"] = b

        b = self.maker.make_button( (100,230), "style_button_scores", self.ops.func_view_scores, func_vars={"view_from":"menu"})
        self.map.objects_menu["func_view_scores"] = b

        # create toys/things for the space
        b = self.maker.make_button( (600,500), "style_button_quit", sys.exit, func_vars=None )
        self.map.objects_menu["func_quit"] = b

        b = self.maker.make_button( (580,350), "style_button_info", self.ops.func_info, func_vars=None )
        self.map.objects_menu["func_info"] = b

    def debug_setup(self):
        """Use this to define the infrastructure that will be needed for the
        module to function. In other words define the objects which affect
        the module's initial entering and/or exiting conditions. Things that
        surround this module, but are also implemented elsewhere. Call this function
        when you want to test one module in isolation.
        """

        # create toys/things for the space
        b = self.maker.make_button( (80,80), "style_button_start", self.ops.func_pick_weapon, func_vars={"pl_name1":"James Brown", "pl_name2":"pl2_Very Long Name For Laughter"} )
        self.map.objects_menu["func_game"] = b
