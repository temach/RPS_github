import pickle
import pygame
from sys import exit

from pprint import pprint

# pprint(self.cp.__dict__)


def debug_dec( func_to_wrap ):
    def print_arguments_wrapper( *args ):       # this wrapped prints the arguments to the function
        print "debugging: Function __{0}__   got args:    {1} ".format(func_to_wrap.__name__, args)
        func_to_wrap( *args )
    return print_arguments_wrapper


def debug( msg ):
    print msg
    print "*"*20, "\n"*3




class Operator(object):
    def __init__(self, control_panel, maker):
        self.cp = control_panel
        self.maker = maker

        self.flags = {}

        self.scores_file = "high_scores.txt"

        n = open(self.scores_file, "rb")
        try: self.flags["scores"] = pickle.load( n )
        except EOFError: self.flags["scores"] = {}      # happens when run for the first time. Because the high_scores.txt file is completely empty.    EOFError = End Of File Error
        n.close()


    def func_view_info(self, func_vars=None):
        debug("Now: Looking at the great makers of this nonsence. Credits for short")


    def func_menu(self, func_vars=None):
        self.cp.active.clear()
        self.cp.activate( self.cp.objects_menu )
        debug("Now: Going to Main menu")


    def func_new_round(self, func_vars=None):
        self.cp.player1.set_weapon( None )
        self.cp.player2.set_weapon( None )
        self.cp.set_current_player( self.cp.player1 )
        self.cp.active.clear()
        self.cp.activate( self.cp.objects_game )
        self.cp.activate( self.cp.objects_pl1_choose_weapon )
        debug("Now: Starting New Round")

    @debug_dec
    def func_quit(self, func_vars="hello try this"):
        debug("Now: Quit Game")
        pygame.quit()
        exit()

    def func_view_scores(self, func_vars):  #fv mush have "view_from" to be "display_winner" or "menu"
        self.cp.objects_scores.clear()

        rect = pygame.Rect( (40,460), (100,90))
        if func_vars["view_from"]=="display_winner":
            img = "next"
            b = self.maker.make_button( rect, self.func_new_round, img, func_vars=None, rescale=True)
            self.cp.deactivate( self.cp.objects_display_winner )
        elif func_vars["view_from"]=="menu":
            img = "menu"
            b = self.maker.make_button( rect, self.func_menu, img, func_vars=None, rescale=True)
            self.cp.deactivate( self.cp.objects_menu )
        self.cp.objects_scores[ b.id ] = b

        text = """   Name _>   Opponent's Name : Number of wins"""
        for p_name, o_info in self.flags["scores"].items():
            text += "\n\n"
            text += "\n" + "\t" + p_name + " has beaten"
            for o_name, o_wins in o_info.items():
                text += "\n" + " "*10 + o_name + " : " + str(o_wins) + "  times"

        # pl1, pl2:wins
        #      pl3:wins


        r = self.maker.make_reader( text, (94, 58), 615, fontsize=20, height=383)
        self.cp.objects_scores[ r.id ] = r

        self.cp.activate( self.cp.objects_scores )
        debug("Now: View High Scores")


    def func_start_game(self, func_vars=None):
        self.cp.set_current_player( self.cp.player1 )
        self.cp.deactivate( self.cp.objects_menu )
        self.cp.activate( self.cp.objects_game )
        self.cp.activate( self.cp.objects_pl1_choose_name )
        debug("Now: Game Starting")


    def func_make_choice_name(self, func_vars):
        if self.cp.cur_player==self.cp.player2:
            self.cp.cur_player.set_name( func_vars["user_input"] )
            debug("Now: Player2 made a Choice,  " + func_vars["user_input"])
            debug("Now: Confirmed Choice of NAME for both")
            self.cp.set_current_player( self.cp.player1 )
            self.cp.deactivate( self.cp.objects_pl2_choose_name )
            self.cp.activate( self.cp.objects_pl1_choose_weapon )
            return

        self.cp.cur_player.set_name( func_vars["user_input"] )
        debug("Now: Made a Choice,  " + func_vars["user_input"])
        self.cp.set_current_player( self.cp.player2 )
        self.cp.deactivate( self.cp.objects_pl1_choose_name )
        self.cp.activate( self.cp.objects_pl2_choose_name)



    def func_make_choice_weapon(self, func_vars):      # expected in func_vars: "weapon" : string
        self.cp.cur_player.set_weapon( func_vars["weapon"] )
        self.cp.activate( self.cp.objects_players_choose_weapons )
        debug("Now: {0} Made a Choice, {1}".format(self.cp.cur_player.get_name(), func_vars["weapon"]))

    def func_confirm_choice_weapon(self):
        if self.cp.cur_player==self.cp.player2:
            debug("Now: Confirmed Choice of Weapon for Both")
            self.cp.deactivate( self.cp.objects_pl2_choose_weapon )
            self.cp.deactivate( self.cp.objects_players_choose_weapons )
            self.display_winner()
            return

        self.cp.set_current_player( self.cp.player2 )
        self.cp.deactivate( self.cp.objects_pl1_choose_weapon )
        self.cp.activate( self.cp.objects_pl2_choose_weapon)
        debug("Now: Confirmed Choice of Weapon")


    def display_winner(self, func_vars=None):
        winner = self.calculate_winner()
        if winner=="draw":
            winner = "Nobody! Its a draw!"

        else:
            if winner=="1":
                winner = self.cp.player1.get_name()
                looser = self.cp.player2.get_name()
            elif winner=="2":
                winner = self.cp.player2.get_name()
                looser = self.cp.player1.get_name()
            try:
                self.flags["scores"][winner][looser] += 1
            except KeyError:
                self.flags["scores"][winner] = {looser:1}

        try:        # delete the previous reader object. Else the self.cp.objects_display_winner dictionary will grow continuously. Because I never nullify it.
            previous_r_id = self.flags["display_winner_reader_id"]
            del self.cp.objects_display_winner[ previous_r_id ]
        except KeyError:
            pass        # this is the first time that the display_winner function is called, so the reader object has not been created yet.

        text = """ And the winner is {0} """.format( winner )           # have to create new every time because I don't have a handle on the reader class
        r = self.maker.make_reader( text, (165, 131), 500, fontsize=20, height=150)
        self.cp.objects_display_winner[ r.id ] = r
        self.flags["display_winner_reader_id"] = r.id

        n = open(self.scores_file, "wb")        # save scores to file
        pickle.dump(self.flags["scores"], n)
        n.close()

        self.cp.deactivate( self.cp.objects_game )
        self.cp.activate( self.cp.objects_display_winner )
        debug("Now: Resolving Battle")


    def calculate_winner(self):
        compare = ["scissors","paper","rock"]
        pl1_score = compare.index(self.cp.player1.current_weapon)
        pl2_score = compare.index(self.cp.player2.current_weapon)

        score = pl1_score - pl2_score       # res = result

        if score == 0:
            winner = "draw"
        elif score in (-1, 2):
            winner = "1"
        elif score in (-2, 1):
            winner = "2"
        else:
            debug("RESULT IS SOMEHTING WIERD:     " + str(winner))

        print "RESOLUTION"
        print self.cp.player1.current_weapon
        print self.cp.player2.current_weapon
        print "ROUND OVER, WINNER IS:   ", winner

        return winner
