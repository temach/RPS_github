#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import os.path
import pygame
from pygame.locals import *
pygame.init()

import constants
import resources


from elements import Button
from util import MakerBasic


class MakerLocal(object):
    def get_surfaces(self, path, rect=False):
        img_types = ("_out.png", "_over.png", "_down.png")
        all_imgs = ( pygame.image.load( path + extra ).convert()  for extra in img_types )

        if rect:
            all_imgs = ( pygame.transform.smoothscale(surf, rect.size) for surf in all_imgs )

        return all_imgs


    def make_button(self, rect, func_to_call, img_name, func_vars=None, rescale=False):
        img_reference = os.path.join( constants.IMAGES_FOLDER_PATH, img_name)

        surf_list = (rescale and self.get_surfaces( img_reference, rect)) or self.get_surfaces( img_reference )
        # To better understand how the above trick works visit "http://www.siafoo.net/article/52" or google "python and/or trick to select values inline"

        b = Button( surf_list, rect, func_to_call, func_vars)
        return b







class MainMenuModule(object):
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
            self.func_game = FunctionsGroup()
            self.func_view_scores = FunctionsGroup()
            self.func_credits = FunctionsGroup()


    class Mapper(object):      # Describes what options you have. In your files you describe how these dictionaries look, the Mapper describes what dictionaries there are.
        def __init__(self):
            self.objects_menu = {}



    pygame.init()

    screen = pygame.display.set_mode( (800,600) )


    operators = Operator()
    mapper = Mapper()
    active = ActiveGroup()

    clock = pygame.time.Clock()


    # Here enter the name of the module
    module = MainMenuModule( active, operators, mapper )
    module.setup()

    active.bind( mapper.objects_menu )



    background = pygame.Surface( screen.get_size() )
    background.fill( (240,240,240) )

    screen.blit( background, (0,0))
    pygame.display.flip()


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
