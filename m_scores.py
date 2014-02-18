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











class HighScore(object):
    def __init__(self, control_panel, operators, mapper):
        self.cp = control_panel
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()


        # specific variables for this cluster
        self.reader = None

        # PlayerName : { OpponentName:NumberOfWins,  OpponentName:NumberOfWins }
        self.scores = util.read_pickle_file( constants.HIGH_SCORES_FILE )





    """ Modify default function behaviour """
    # What are some of the things that will happen (in terms of this class) when Someone calls "func_mein_menu"
    def func_menu(self, func_vars=None):
        self.cp.unbind( self.map.objects_scores )


    # What are some of the things that will happen when someone calls "func_view_scores"
    def func_view_scores(self, func_vars=None):
        text = """   Name _>   Opponent's Name : Number of wins"""

        for p_name, o_info in self.scores.items():
            text += "\n\n\t {0} has beaten".format( p_name )
            for o_name, o_wins in o_info.items():
                text += "\n\t\t\t {0} : {1}   times".format( o_name, str(o_wins))


        self.reader.update_text( text )     # this is using the handle to the reader object created by the self.setup() function

        self.cp.bind( self.map.objects_scores )
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
        self.map.objects_scores["reader"] = r
        self.reader = r     # simply a local handle to the reader (shortcut)


        rect = pygame.Rect( (80,180), (160,60))
        img = "scores"
        b = self.maker.make_button(rect, self.ops.func_view_scores, img, func_vars={"view_from":"menu"}, rescale=True)
        self.map.objects_menu["func_view_scores"] = b

