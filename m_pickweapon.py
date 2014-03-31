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



class PickWeapon( util.ModuleBasic ):
    text_pl1 = """
                    Time to Choose you Tool! Player 1
"""

    text_pl2 = """
                    Now its time!
                     for player2
                         to
                    find his way!
"""


    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()


        # specific variables for this cluster
        self.reader = None

        self.pl_name1 = None       # player1 name
        self.pl1_weapon = None
        self.pl_name2 = None
        self.pl2_weapon = None

        self.cur_pl = 1


        self._objects_pick_weapon1 = {}
        self._objects_pick_weapon2 = {}


    """ Modify default function behaviour """
    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_show_winner(self, func_vars=None):
        self.cp.unbind( self.map.objects_pick_weapon )
        self.cp.unbind( self._objects_pick_weapon1 )
        self.cp.unbind( self._objects_pick_weapon2 )

    def func_pick_weapon(self, func_vars=None):
        self.cur_pl = 1
        if "pl_name1" in func_vars:     # if there is one name, there are two.
            self.pl_name1 = func_vars["pl_name1"]
            self.pl_name2 = func_vars["pl_name2"]
            print "Got names   ", self.pl_name1, "   ", self.pl_name2
        self.cp.bind( self.map.objects_pick_weapon )
        self.cp.bind( self._objects_pick_weapon1 )
    """ End modify section """



    def _func_submit_weapon(self, func_vars=None):
        if self.cur_pl==1:
            self.pl1_weapon = func_vars["weapon"]
            print "player1 weapon", self.pl1_weapon

        else:       # cur_pl==2
            self.pl2_weapon = func_vars["weapon"]
            print "player2 weapon", self.pl2_weapon


    def _func_change_active_player(self, func_vars=None):
        assert func_vars["change_to_player"] in (1, 2, False), "Problem: want to change to some wierd player number."

        self.cur_pl = func_vars["change_to_player"]

        if self.cur_pl==1:
            self.reader.update_text( self.text_pl1 )
            self.pl1_weapon = None
            self.cp.unbind( self._objects_pick_weapon2 )
            self.cp.bind( self._objects_pick_weapon1 )

        if self.cur_pl==2:
            self.reader.update_text( self.text_pl2 )
            self.pl2_weapon = None
            self.cp.unbind( self._objects_pick_weapon1 )
            self.cp.bind( self._objects_pick_weapon2 )

        if self.cur_pl is False:    # both pl1 and pl2 have chosen weapons, now its time to resolve battle and show winner.
            self.ops.func_show_winner( {    "pl_name1":self.pl_name1, "pl_name2":self.pl_name2,
                                            "pl1_weapon":self.pl1_weapon, "pl2_weapon":self.pl2_weapon,} )






    """ Modify default object existence """
    def setup(self):
        self.ops.func_pick_weapon.append( self.func_pick_weapon )
        self.ops.func_show_winner.append( self.func_show_winner )

        # things that exist within the space
        rect = pygame.Rect( (40,460), (100,90))
        img = "restart"
        b = self.maker.make_button( rect, self._func_change_active_player, img, func_vars={"change_to_player":1}, rescale=True)
        self.map.objects_pick_weapon["func_restart_round"] = b

        r = self.maker.make_reader( self.text_pl1, (94, 58), 600, "style_reader1")
        self.map.objects_pick_weapon["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)




        rect = pygame.Rect( (186,170), (140,70))
        img = "rock"
        b = self.maker.make_button( rect, self._func_submit_weapon, img, {"weapon":"rock"}, True)
        self._objects_pick_weapon1["weapon_choice1"] = b

        rect = pygame.Rect( (331,176), (140,70))
        img = "paper"
        b = self.maker.make_button( rect, self._func_submit_weapon, img, {"weapon":"paper"}, True)
        self._objects_pick_weapon1["weapon_choice2"] = b

        rect = pygame.Rect( (490,170), (140,70))
        img = "scissors"
        b = self.maker.make_button( rect, self._func_submit_weapon, img, {"weapon":"scissors"}, True)
        self._objects_pick_weapon1["weapon_choice3"] = b

        rect = pygame.Rect( (696,173), (67,65))
        img = "confirm"
        b = self.maker.make_button( rect, self._func_change_active_player, img, func_vars={"change_to_player":2}, rescale=True)
        self._objects_pick_weapon1["next_pl"] = b



        rect = pygame.Rect( (186,294), (140,70))
        img = "rock"
        b = self.maker.make_button( rect, self._func_submit_weapon, img, {"weapon":"rock"}, True)
        self._objects_pick_weapon2["weapon_choice1"] = b

        rect = pygame.Rect( (331,294), (140,70))
        img = "paper"
        b = self.maker.make_button( rect, self._func_submit_weapon, img, {"weapon":"paper"}, True)
        self._objects_pick_weapon2["weapon_choice2"] = b

        rect = pygame.Rect( (490,294), (140,70))
        img = "scissors"
        b = self.maker.make_button( rect, self._func_submit_weapon, img, {"weapon":"scissors"}, True)
        self._objects_pick_weapon2["weapon_choice3"] = b

        rect = pygame.Rect( (694,297), (83,72))
        img = "confirm"
        b = self.maker.make_button( rect, self._func_change_active_player, img, func_vars={"change_to_player":False}, rescale=True)
        self._objects_pick_weapon2["next_pl"] = b



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
        b = self.maker.make_button(rect, self.ops.func_pick_weapon, img, func_vars={"pl_name1":"TestingArtem", "pl_name2":"TestingPlayer2Name"}, rescale=True)
        self.map.objects_menu["func_game"] = b



