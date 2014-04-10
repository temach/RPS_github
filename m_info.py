#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import pygame
import pygame.locals as PL

from elements import Button, Reader
import util
import small_util



class MakerLocal( util.MakerBasic ):
    pass



class Info( util.ModuleBasic ):

    info_text = """
        Who made this GAME?!
            Artem did.
            Blame him.
            Thank him.
               The
               End
               ...
"""

    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()

        # specific variables for this cluster
        self.reader = None


    """ Modify default function behaviour """
    def func_main_menu(self, func_vars=None):
        self.cp.unbind( self.map.objects_info )

    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_info(self, func_vars=None):
        self.cp.bind( self.map.objects_info )
    """ End modify section """




    """ Modify default object existence """
    def setup(self):
        self.ops.func_main_menu.append( self.func_main_menu )
        self.ops.func_info.append( self.func_info )

        # things that exist within the space
        r = self.maker.make_reader( self.info_text, (94, 58), 600, "style_reader1")
        self.map.objects_info["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)


        b = self.maker.make_button( (40,460), "style_button_menu", self.ops.func_main_menu, func_vars=None )
        self.map.objects_info["main_menu"] = b



    def debug_setup(self):
        """Use this to define the infrastructure that will be needed for the
        module to function. In other words define the objects which affect
        the module's initial entering and/or exiting conditions. Things that
        surround this module, but are also implemented elsewhere. Call this function
        when you want to test one module in isolation.
        """

        # create toys/things for the space
        info = style.style_button_start
        b = self.maker.make_button( pos=(150,80),
                                    style_name="style_button_info",
                                    func=self.ops.func_info,
                                    func_vars=None,
                                    rescale=True )

        self.map.objects_menu["func_info"] = b





