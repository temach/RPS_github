__all__=["Maker"]

import pygame
import agk

import os.path


from elements import Button, Text, Reader, Form, FormPrompter



class Maker(object):
    def __init__(self):
        self.ops = None     # This is assigned separately during initialisation in the ControlPanel


    def make_objects_menu(self):
        objects_menu = {}

        rect = pygame.Rect( (80,80), (160,60))
        img = "start"
        b = self.make_button(rect, self.ops.func_start_game, img, func_vars=None, rescale=True)
        objects_menu[b.id] = b

        rect = pygame.Rect( (560,410), (160,60))
        img = "info"
        b = self.make_button(rect, self.ops.func_view_info, img, func_vars=None, rescale=True)
        objects_menu[b.id] = b

        rect = pygame.Rect( (80,180), (160,60))
        img = "scores"
        b = self.make_button(rect, self.ops.func_view_scores, img, func_vars={"view_from":"menu"}, rescale=True)
        objects_menu[b.id] = b

        rect = pygame.Rect( (560,520), (160,60))
        img = "quit"
        b = self.make_button(rect, self.ops.func_quit, img, func_vars=None, rescale=True)
        objects_menu[b.id] = b

        return objects_menu


    def make_objects_game(self):
        objs = {}

        rect = pygame.Rect( (40,460), (100,90))
        img = "menu"
        b = self.make_button( rect, self.ops.func_menu, img, func_vars=None, rescale=True)
        objs[b.id] = b

        return objs




    def make_objects_pl1_choose_name(self):
        objs = {}

        text = """Hello and welcome to da battle arena.
Here any two things can fight.
Player 1 should enter his name
        """
        r = self.make_reader( text, (110, 24), 613, fontsize=15, height=144)
        objs[ r.id ] = r

        name_f = self.make_form((185, 209), 355, fontsize=15, height=70)
        objs[ name_f.id ] = name_f

        rect = pygame.Rect((567, 212), (46,46))
        img = "confirm"
        fp = self.make_form_prompter(name_f, rect, self.ops.func_make_choice_name, img, True)
        objs[ fp.id ] = fp

        return objs




    def make_objects_pl2_choose_name(self):
        objs = {}

        text = """
Now Player2 can choose his/her/its name
Notice that because player2 had to wait for player1 he can choose a longer name.
        """
        r = self.make_reader( text, (110, 24), 613, fontsize=15, height=144)
        objs[ r.id ] = r

        name_f = self.make_form((222, 309), 480, fontsize=15, height=70)
        objs[ name_f.id ] = name_f

        rect = pygame.Rect((731, 312), (46,46))
        img = "confirm"
        fp = self.make_form_prompter(name_f, rect, self.ops.func_make_choice_name, img, True)
        objs[ fp.id ] = fp

        return objs

    def make_objects_players_choose_weapons(self):
        objs = {}

        rect = pygame.Rect( (656,474), (94,47))
        img = "restart"
        b = self.make_button( rect, self.ops.func_new_round, img, func_vars=None, rescale=True)
        objs[b.id] = b

        return objs


    def make_objects_pl1_choose_weapon(self):
        objs = {}

        text = """
Now Player1 can choose a weapon. Rock seems like an obvious choice.
To make a choice just click on one, it will look like nothing has happened, but that is the point!
        Afterward click the confirm button to pass the turn.
        """
        r = self.make_reader( text, (110, 24), 613, fontsize=15, height=144)
        objs[ r.id ] = r

        rect = pygame.Rect( (186,170), (140,70))
        img = "rock"
        b = self.make_button( rect, self.ops.func_make_choice_weapon, img, {"weapon":"rock"}, True)
        objs[b.id] = b

        rect = pygame.Rect( (331,176), (140,70))
        img = "paper"
        b = self.make_button( rect, self.ops.func_make_choice_weapon, img, {"weapon":"paper"}, True)
        objs[b.id] = b

        rect = pygame.Rect( (490,170), (140,70))
        img = "scissors"
        b = self.make_button( rect, self.ops.func_make_choice_weapon, img, {"weapon":"scissors"}, True)
        objs[b.id] = b

        rect = pygame.Rect( (696,173), (67,65))
        img = "confirm"
        b = self.make_button( rect, self.ops.func_confirm_choice_weapon, img, func_vars=None, rescale=True)
        objs[b.id] = b

        return objs


    def make_objects_pl2_choose_weapon(self):
        objs = {}

        text = """
        Finally Player2 can pick a weapon.
        How delightful.
        """
        r = self.make_reader( text, (110, 24), 613, fontsize=15, height=144)
        objs[ r.id ] = r

        rect = pygame.Rect( (186,294), (140,70))
        img = "rock"
        b = self.make_button( rect, self.ops.func_make_choice_weapon, img, {"weapon":"rock"}, True)
        objs[b.id] = b

        rect = pygame.Rect( (331,294), (140,70))
        img = "paper"
        b = self.make_button( rect, self.ops.func_make_choice_weapon, img, {"weapon":"paper"}, True)
        objs[b.id] = b

        rect = pygame.Rect( (490,294), (140,70))
        img = "scissors"
        b = self.make_button( rect, self.ops.func_make_choice_weapon, img, {"weapon":"scissors"}, True)
        objs[b.id] = b

        rect = pygame.Rect( (694,297), (83,72))
        img = "confirm"
        b = self.make_button( rect, self.ops.func_confirm_choice_weapon, img, func_vars=None, rescale=True)
        objs[b.id] = b

        return objs



    def make_objects_display_winner(self):
        objs = {}

        rect = pygame.Rect( (40,460), (100,64))
        img = "menu"
        b = self.make_button( rect, self.ops.func_menu, img, func_vars=None, rescale=True)
        objs[b.id] = b

        rect = pygame.Rect( (656,474), (94,47))
        img = "next"
        b = self.make_button( rect, self.ops.func_new_round, img, func_vars=None, rescale=True)
        objs[b.id] = b

        rect = pygame.Rect( (560,309), (110,64))
        img = "scores"
        b = self.make_button( rect, self.ops.func_view_scores, img, func_vars={"view_from":"display_winner"}, rescale=True)
        objs[b.id] = b

        return objs



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



    def make_form(self, pos, width,
                        fontsize=12,
                        height=None,
                        font=None,
                        bg=(100,100,100),
                        fgcolor=(250,250,250),
                        hlcolor=(250,190,150,50),
                        curscolor=(190,0,10),
                        maxlines=0):
        """ Creates a form, but remember that a form's input can not be grabbed without a form confirmation button"""
        f = Form( pos, width, fontsize, height, font, bg, fgcolor, hlcolor, curscolor, maxlines)
        return f



    def make_form_prompter(self, some_form, rect, func_to_call,
                                 img_name="confirm",
                                 rescale=False):
        """ Used to grab the form's input and send to any function"""
        img_folder_path = os.path.join("img", img_name)
        out = pygame.image.load( img_folder_path + "_out.png"   ).convert()
        over = pygame.image.load( img_folder_path + "_over.png" ).convert()
        down = pygame.image.load( img_folder_path + "_down.png" ).convert()

        if rescale==True:
            out = pygame.transform.smoothscale(out, rect.size)
            over = pygame.transform.smoothscale(over, rect.size)
            down = pygame.transform.smoothscale(down, rect.size)

        fm = FormPrompter( [out,over,down], rect, func_to_call, {"user_input":""}, some_form )    # the "some_form" here referes to any Form that would be used to grab the user's input
        return fm


    def make_button(self, rect, func_to_call, img_name, func_vars=None, rescale=False):
        img_folder_path = os.path.join("img", img_name)
        out = pygame.image.load( img_folder_path + "_out.png"   ).convert()
        over = pygame.image.load( img_folder_path + "_over.png" ).convert()
        down = pygame.image.load( img_folder_path + "_down.png" ).convert()

        if rescale==True:
            out = pygame.transform.smoothscale(out, rect.size)
            over = pygame.transform.smoothscale(over, rect.size)
            down = pygame.transform.smoothscale(down, rect.size)

        b = Button( [out, over, down], rect, func_to_call, func_vars)
        return b









"""
        rect = pygame.Rect( (300,100), (300,300))
        text = "This is where the game would be played, So the sides would be choosing theur weapons. After they have choosen their names of course."
        f_obj = pygame.font.SysFont("arial", 10)
        t = Text(rect, text, (100,100,210), f_obj)
        objects_credits[t.id] = t
"""
