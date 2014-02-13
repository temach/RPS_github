#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import pickle
import pygame
from pygame.locals import *
pygame.init()



from elements import Button, Reader






def get_filled(surf, col):
    s = surf.copy()
    s.fill( col )
    return s



class MakerLocal(object):

    def make_reader(self, text, pos, width,
                            fontsize=15,
                            height=None,
                            font=None,
                            bg=(100,100,100),
                            fgcolor=(255,255,255),
                            hlcolor=(255,10,150,100),
                            split=False):
        """ pos and width are necessary. """
        if not type(text)==unicode:
            text = unicode(text.expandtabs(4),'utf8')
        t = Reader( text, pos, width, fontsize, height, font, bg, fgcolor, hlcolor, split)
        return t


    def make_button(self, rect, func_to_call, img_name, func_vars=None, rescale=False):
        #img_folder_path = os.path.join("img", img_name)
        some_surf = pygame.Surface((50,50))
        out = get_filled( some_surf, (100,100,100) )
        over = get_filled( some_surf, (100,200,100) )
        down = get_filled( some_surf, (100,100,200) )

        if rescale==True:
            out = pygame.transform.smoothscale(out, rect.size)
            over = pygame.transform.smoothscale(over, rect.size)
            down = pygame.transform.smoothscale(down, rect.size)

        b = Button( [out, over, down], rect, func_to_call, func_vars)
        return b











class HighScore(object):
    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()


        # specific variables for this cluster
        self.reader = None
        self.flags = {}
        self.scores_file = "high_scores.txt"

        n = open(self.scores_file, "rb")
        try: self.flags["scores"] = pickle.load( n )
        except EOFError: self.flags["scores"] = {}      # happens when run for the first time. Because the high_scores.txt file is completely empty.    EOFError = End Of File Error
        n.close()



    """ Modify default function behaviour """
    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_menu(self, func_vars=None):
        self.cp.deactivate( self.map.objects_scores )
        self.cp.activate( self.map.objects_menu )

    # What are some of the things that will happen when someone calls "func_view_scores"
    def func_view_scores(self, func_vars=None):
        self.cp.deactivate( self.map.objects_menu )

        text = """   Name _>   Opponent's Name : Number of wins"""
        for p_name, o_info in self.flags["scores"].items():
            text += "\n\n"
            text += "\n" + "\t" + p_name + " has beaten"
            for o_name, o_wins in o_info.items():
                text += "\n" + " "*10 + o_name + " : " + str(o_wins) + "  times"

        self.reader.update_text( text )     # this is using the handle to the reader object created by the self.setup() function

        self.cp.activate( self.map.objects_scores )
    """ End modify section """




    """ Modify default object existence """
    def setup(self):
        self.ops.view_scores.append( self.func_view_scores )
        self.ops.main_menu.append( self.func_menu )


        # things that exist within the space
        rect = pygame.Rect( (40,460), (100,90))
        img = "menu"
        b = self.maker.make_button( rect, self.ops.func_main_menu, img, func_vars=None, rescale=True)
        self.map.objects_scores["func_main_menu"] = b

        text = ""
        r = self.maker.make_reader( text, (94, 58), 615, fontsize=20, height=383)
        self.reader = r     # simply a handle to the reader (shortcut)
        self.map.objects_scores["reader"] = r


        rect = pygame.Rect( (80,180), (160,60))
        img = "scores"
        b = self.maker.make_button(rect, self.ops.func_view_scores, img, func_vars={"view_from":"menu"}, rescale=True)
        self.map.objects_menu["func_view_scores"] = b

