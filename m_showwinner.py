#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import pygame
import pygame.locals as PL
import collections as col

from elements import Button, Reader
import util
import small_util




class MakerLocal( util.MakerBasic ):
    pass



class ShowWinner( util.ModuleBasic ):
    Player = col.namedtuple('Player', ['name', 'weapon'])

    win_text = """
        And the Winner is {0}

"""

    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()


        # specific variables for this cluster
        self.reader = None

        # PlayerName : { OpponentName1:NumberOfWins,  OpponentName2:NumberOfWins }
        self.scores = small_util.read_pickle_file( "high_scores.txt" ) or col.OrderedDict()
        self.scores_file = "high_scores.txt"



    """ Modify default function behaviour """
    def func_main_menu(self, func_vars=None):
        self.cp.unbind( self.map.objects_show_winner )

    def func_view_scores(self, func_vars=None):
        self.cp.unbind( self.map.objects_show_winner )

    def func_pick_weapon(self, func_vars=None):
        self.cp.unbind( self.map.objects_show_winner )


    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_show_winner(self, func_vars=None):
        self.cp.bind( self.map.objects_show_winner )

        # if func_vars is None then we just re-show the previous winner, else
        if func_vars!=None:
            pl1 = self.Player( func_vars["pl_name1"], func_vars["pl1_weapon"] )
            pl2 = self.Player( func_vars["pl_name2"], func_vars["pl2_weapon"] )

            result = self._func_judge_battle( pl1, pl2)

            try:
                self.winner_name, looser_name = result     # cache the winner variable for future reference
            except TypeError:
                self.winner_name = "Nobody! Its a draw!"

            else:      # try worked well, so change stats and save to disk, because its not a draw.
                print "saving data in ShowWinner"
                self.scores.setdefault( self.winner_name, col.defaultdict( int ) )[looser_name] += 1
                small_util.write_pickle_file( "high_scores.txt", self.scores )


        text = self.win_text.format( self.winner_name )
        self.reader.update_text( text )
    """ End modify section """




    def _func_judge_battle(self, pl1, pl2 ):
        compare = ("scissors","paper","rock")
        pl1_score = compare.index( pl1.weapon )
        pl2_score = compare.index( pl2.weapon )
        score = pl1_score - pl2_score

        if score == 0:
            return None
        elif score in (-1, 2):
            return (pl1.name, pl2.name)
        elif score in (-2, 1):
            return (pl2.name, pl1.name)
        print "RESULT IS SOMEHTING WIERD:     ", score      # just to debug




    """ Modify default object existence """
    def setup(self):
        self.ops.func_pick_weapon.append( self.func_pick_weapon )
        self.ops.func_show_winner.append( self.func_show_winner )
        self.ops.func_main_menu.append( self.func_main_menu )
        self.ops.func_view_scores.append( self.func_view_scores )


        # things that exist within the space
        text = ""
        r = self.maker.make_reader( text, (94, 58), 600, "style_reader1")
        self.map.objects_show_winner["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)


        b = self.maker.make_button( (40,460), "style_button_menu", self.ops.func_main_menu, func_vars=None )
        self.map.objects_show_winner["main_menu"] = b

        # the "func_vars" for this button has to be an empty dict, see "func_pick_weapon" in "m_pickweapon.py"
        b = self.maker.make_button( (656,474), "style_button_next", self.ops.func_pick_weapon, func_vars={} )
        self.map.objects_show_winner["next"] = b

        b = self.maker.make_button( (560,309), "style_button_scores", self.ops.func_view_scores, func_vars={"view_from":"display_winner"} )
        self.map.objects_show_winner["view_scores"] = b



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
        info = style.style_button_start
        b = self.maker.make_button( pos=(80,80),
                                    style_name="style_button_start",
                                    func=self.ops.func_show_winner,
                                    func_vars={"pl_name1":"ArtemIsTesting", "pl_name2":"SomeWinner", "pl1_weapon":"rock", "pl2_weapon":"paper" },
                                    rescale=True )

        self.map.objects_menu["func_game"] = b




