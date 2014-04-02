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
        Time to Choose you Tool Mr. {name}!
"""

    text_pl2 = """
                    Now its time!
                     for {name}
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

    def func_main_menu( self, func_vars=None):
        self.cp.unbind( self.map.objects_pick_weapon )
        self.cp.unbind( self._objects_pick_weapon1 )
        self.cp.unbind( self._objects_pick_weapon2 )


    def func_pick_weapon(self, func_vars={}):
        self.cur_pl = 1

        # if there is one name, there are two.
        if "pl_name1" in func_vars:
            self.pl_name1, self.pl_name2 = func_vars["pl_name1"], func_vars["pl_name2"]
            self.text_pl1, self.text_pl2 = self.text_pl1.format( name=self.pl_name1 ), self.text_pl2.format( name=self.pl_name2 )

            self._func_change_active_player( {"change_to_player":1} )
            print "Got names   ", self.pl_name1, "   ", self.pl_name2

        # if there are no names we just show the cached info from latest session.
        self.cp.bind( self.map.objects_pick_weapon )
        self.cp.bind( self._objects_pick_weapon1 )
    """ End modify section """



    def _func_submit_weapon(self, func_vars=None):
        if self.cur_pl==1:
            self.pl1_weapon = func_vars["weapon"]
            print "player1 weapon", self.pl1_weapon

        else:     # if cur_pl==2
            self.pl2_weapon = func_vars["weapon"]
            print "player2 weapon", self.pl2_weapon


    def _func_change_active_player(self, func_vars=None):
        assert func_vars["change_to_player"] in (1, 2, False), "Problem: want to change to some wierd player number. "

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
        self.ops.func_main_menu.append( self.func_main_menu )

        # things that exist within the space
        b = self.maker.make_button( (50,460), "style_button_menu", self.ops.func_main_menu, func_vars=None, rescale=True)
        self.map.objects_pick_weapon["func_main_menu"] = b

        r = self.maker.make_reader( self.text_pl1, (94, 58), 600, "style_reader1")
        self.map.objects_pick_weapon["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)



        b = self.maker.make_button( (186,170), "style_button_rock", self._func_submit_weapon, {"weapon":"rock"}, True)
        self._objects_pick_weapon1["weapon_choice1"] = b
        b = self.maker.make_button( (331,176), "style_button_paper", self._func_submit_weapon, {"weapon":"paper"}, True)
        self._objects_pick_weapon1["weapon_choice2"] = b
        b = self.maker.make_button( (490,170), "style_button_scissors", self._func_submit_weapon, {"weapon":"scissors"}, True)
        self._objects_pick_weapon1["weapon_choice3"] = b

        b = self.maker.make_button( (696,173), "style_button_confirm", self._func_change_active_player, func_vars={"change_to_player":2}, rescale=True)
        self._objects_pick_weapon1["next_pl"] = b


        b = self.maker.make_button( (186,294), "style_button_rock", self._func_submit_weapon, {"weapon":"rock"}, True)
        self._objects_pick_weapon2["weapon_choice1"] = b
        b = self.maker.make_button( (331,294), "style_button_paper", self._func_submit_weapon, {"weapon":"paper"}, True)
        self._objects_pick_weapon2["weapon_choice2"] = b
        b = self.maker.make_button( (490,294), "style_button_scissors", self._func_submit_weapon, {"weapon":"scissors"}, True)
        self._objects_pick_weapon2["weapon_choice3"] = b

        b = self.maker.make_button( (694,297), "style_button_confirm", self._func_change_active_player, func_vars={"change_to_player":False}, rescale=True)
        self._objects_pick_weapon2["next_pl"] = b

        # transfer choice of weapon back to player1
        b = self.maker.make_button( (600,460), "style_button_restart", self._func_change_active_player, func_vars={"change_to_player":1}, rescale=True)
        self._objects_pick_weapon2["func_restart_round"] = b


    def debug_setup(self):
        """Use this to define the infrastructure that will be needed for the
        module to function. In other words define the objects which affect
        the module's initial entering and/or exiting conditions. Things that
        surround this module, but are also implemented elsewhere. Call this function
        when you want to test one module in isolation.
        """

        # create toys/things for the space
        b = self.maker.make_button( (80,80), "style_button_start", self.ops.func_pick_weapon, func_vars={"pl_name1":"James Brown", "pl_name2":"pl2_Very Long Name For Laughter"}, rescale=True)
        self.map.objects_menu["func_game"] = b



