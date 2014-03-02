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



class PickName( util.ModuleBasic ):
    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()


        # specific variables for this cluster
        self.reader = None
        self.pl_name1 = None       # player1 name
        self.pl_name2 = None
        self.cur_pl = 1


        text_pl1 = """
                    Hello, welcome,
    You are player1, can you choose your name now?
         Make sure not to make typing errors
"""

        text_pl2 = """
                    Now its time!
                     for player2
                         to
                       choose!
"""


    """ Modify default function behaviour """
    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_menu(self, func_vars=None):
        self.cp.unbind( self.map.objects_pick_weapon )

    def func_pick_weapon(self, func_vars=None):
        self.pl_name1 = func_vars["pl_name1"]
        self.pl_name2 = func_vars["pl_name2"]
        self.cp.bind( self.map.objects_pick_weapon )


    # What are some of the things that will happen when someone calls "func_view_scores"
    def func_submit_weapon(self, func_vars=None):
        if self.cur_pl==2:
            self.pl2_weapon = func_vars["user_input"]

            self.cp.func_pick_weapon(  {"pl_name1":self.pl_name1, "pl_name2":self.pl_name2}  )

        self.pl_name1 = func_vars["user_input"]
        print "player1 name", self.pl_name1

        self.cur_pl = 2
        self.reader.update_text( text_pl2 )

    """ End modify section """





    """ Modify default object existence """
    def setup(self):
        self.ops.func_main_menu.append( self.func_menu )
        self.ops.func_submit_name.append( self.func_submit_name )

        # things that exist within the space
        rect = pygame.Rect( (40,460), (100,90))
        img = "menu"
        b = self.maker.make_button( rect, self.ops.func_main_menu, img, func_vars=None, rescale=True)
        self.map.objects_pick_name["func_main_menu"] = b


        text = ""
        r = self.maker.make_reader( text, (94, 58), 600, "hello artem this will be a string with style_name")
        self.map.objects_pick_name["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)


        f1 = self.maker.make_form( )
        self.map.objects_pick_name1["form1"] = f1
        fp1 = self.maker.make_form_prompter()
        self.map.objects_pick_name1["form_prompter1"] = fp1


        f2 = self.maker.make_form()
        self.map.objects_pick_name2["form2"] = f2
        fp2 = self.maker.make_form_prompter()
        self.map.objects_pick_name2["form_prompter2"] = fp2




    def debug_setup(self):
        """Use this to define the infrastructure that will be needed for the
        module to function. In other words define the objects which affect
        the module's initial entering and/or exiting conditions. Things that
        surround this module, but are also implemented elsewhere. Call this function
        when you want to test one module in isolation.
        """

        # create toys/things for the space
        rect = pygame.Rect( (80,80), (160,60))
        img = "start"
        b = self.maker.make_button(rect, self.ops.func_game, img, func_vars=None, rescale=True)
        self.map.objects_menu["func_game"] = b



