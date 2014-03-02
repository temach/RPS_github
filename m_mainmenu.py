#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import pygame
import pygame.locals as PL

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



    # Go to game, finishing function
    def func_view_scores(self, func_vars=None):
        self.active.unbind( self.map.objects_menu )

    # Go to game, finishing function
    def func_game(self, func_vars=None):
        self.active.unbind( self.map.objects_menu )

    # This is an entry function
    def func_main_menu(self, func_vars=None):
        self.active.bind( self.map.objects_menu )



    def setup(self):
        self.ops.func_view_scores.append( self.func_view_scores )
        self.ops.func_main_menu.append( self.func_main_menu )
        self.ops.func_game.append( self.func_game )


        # create toys/things for the space
        rect = pygame.Rect( (80,80), (160,60))
        img = "start"
        b = self.maker.make_button(rect, self.ops.func_game, img, func_vars=None, rescale=True)
        self.map.objects_menu["func_game"] = b

        rect = pygame.Rect( (100,230), (160,60))
        img = "scores"
        b = self.maker.make_button(rect, self.ops.func_view_scores, img, func_vars={"view_from":"menu"}, rescale=True)
        self.map.objects_menu["func_view_scores"] = b
