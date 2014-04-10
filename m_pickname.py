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
    #def __init__(self):
    #    super( MakerLocal, self ).change_menu_imgs()
    #    super( MakerLocal, self ).__init__()



class PickName( util.ModuleBasic ):
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

        self._objects_pick_name1 = {}
        self._objects_pick_name2 = {}

        '''
        self.text_pl1 = """
                    Hello, welcome,
    You are player1, can you choose your name now?
         Make sure not to make typing errors
"""

        self.text_pl2 = """
                    Now its time!
                     for player2
                         to
                       choose!
"""
        '''

    """ Modify default function behaviour """
    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_menu(self, func_vars=None):
        #start debug
        #self.cp.bind( self.map.objects_menu )
        #db end
        self.cur_pl=1
        self.cp.unbind( self.map.objects_pick_name )
        self.cp.unbind( self._objects_pick_name1 )
        self.cp.unbind( self._objects_pick_name2 )

    def func_game(self, func_vars=None):
        #start debug
        #self.cp.unbind( self.map.objects_menu )
        #db end
        self.reader.update_text( self.text_pl1 )
        self.cp.bind( self.map.objects_pick_name )
        self.cp.bind( self._objects_pick_name1 )    # this is local, watch for "_" in name start


    def func_pick_weapon(self, func_vars=None):
        self.cp.unbind( self.map.objects_pick_name )
        self.cp.unbind( self._objects_pick_name1 )
        self.cp.unbind( self._objects_pick_name2 )

    """ End modify section """

    """ Start local section """
    # What are some of the things that will happen when someone calls "func_view_scores"
    def _func_submit_name(self, func_vars=None):
        if not self._check_name( func_vars["user_input"].strip() ):
            return

        if self.cur_pl==1:
            self.pl_name1 = func_vars["user_input"].strip()
            print "name 1  ___", self.pl_name1, "___"
            self.cur_pl = 2
            self.reader.update_text( self.text_pl2 )
            self.cp.unbind( self._objects_pick_name1)
            self.cp.bind( self._objects_pick_name2)

        else:   # if cur_pl == 2
            self.pl_name2 = func_vars["user_input"].strip()
            print "name2 __", self.pl_name2, "___"
            self.ops.func_pick_weapon(  {"pl_name1":self.pl_name1, "pl_name2":self.pl_name2}  )


    def _check_name( self, name_str ):
        return ( name_str.isalnum() and len(name_str)<15 )







    """ Modify default object existence """
    def setup(self):
        self.ops.func_main_menu.append( self.func_menu )
        self.ops.func_game.append( self.func_game )
        self.ops.func_pick_weapon.append( self.func_pick_weapon )


        # things that exist within the space
        b = self.maker.make_button( (40,460), "style_button_menu", self.ops.func_main_menu, func_vars=None )
        self.map.objects_pick_name["func_main_menu"] = b

        text = ""
        r = self.maker.make_reader( text, (130, 58), 600, "style_reader1")
        self.map.objects_pick_name["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)


        f1 = self.maker.make_form( (100, 209), "style_form3" )
        self._objects_pick_name1["form1"] = f1

        fp1_rect = pygame.Rect( (567, 212), (46,46) )
        fp1 = self.maker.make_form_prompter( f1, fp1_rect, self._func_submit_name )
        self._objects_pick_name1["form_prompter1"] = fp1


        f2 = self.maker.make_form( (222, 309), "style_form3" )
        self._objects_pick_name2["form2"] = f2

        fp2_rect = pygame.Rect( (701, 312), (46,46) )
        fp2 = self.maker.make_form_prompter( f2, fp2_rect, self._func_submit_name )
        self._objects_pick_name2["form_prompter2"] = fp2




    def debug_setup(self):
        """Use this to define the infrastructure that will be needed for the
        module to function. In other words define the objects which affect
        the module's initial entering and/or exiting conditions. Things that
        surround this module, but are also implemented elsewhere. Call this function
        when you want to test one module in isolation.
        """


        # create toys/things for the space
        b = self.maker.make_button( (80,50), "style_button_game", self.ops.func_game, func_vars=None )
        self.map.objects_menu["func_game"] = b


