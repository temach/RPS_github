#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import os.path
import pygame
import pygame.locals as PL

import util
from elements import ElementBase





class Splash( ElementBase ):
    def __init__(self, func_to_call, func_vars):
        ElementBase.__init__(self)

        self.id = id(self)
        self.rect = pygame.Rect( 0,0,0,0 )
        self.func = func_to_call
        self.func_vars = func_vars
        self.has_run = False
        self.screen = None


    def run(self):
        print "run is called"
        if self.has_run==False and self.screen!=None:
            self.func_vars["screen"] = self.screen
            print "calling func"
            self.func( self.func_vars )
            self.has_run = True

    def render(self, screen):
        print "render is called"
        if self.screen==None:
            self.rect = screen.get_rect()
            self.screen = screen    # capture the screen, later add it to your func vars and pass it to the func_splash_screen()
            print "screen is set"
        return screen.get_rect()



class MakerLocal( util.MakerBasic ):

    def make_splash(self, func_to_call, func_vars):
        sp = Splash( func_to_call, func_vars )
        return sp






class SplashModule( util.ModuleBasic ):

    def __init__(self, active, operators, mapper):
        self.active = active
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()

        self.music_path = os.path.join("data", "splash.ogg")
        self.image_path = os.path.join("data", "gimpysplash1.png")


    def func_main_menu(self, func_vars):
        self.active.unbind( self.map.objects_splash_screen )
        self.active.bind( self.map.objects_menu )


    def func_splash_screen(self, func_vars=None):       # entry point
        """
        Show the splash screen.
        This is called once when the game is first started.
        """
        screen = func_vars["screen"]

        pygame.mixer.music.load( self.music_path )
        pygame.mixer.music.play()

        # Slowly fade the splash screen image from white to opaque.
        splash = pygame.image.load( self.image_path ).convert()
        splash = pygame.transform.smoothscale( splash, (800,600) )

        for i in range(27):
            pygame.event.pump()     # tell OS that we are processing events otherwise it thinks the app is frozen
            splash.set_alpha(i)
            screen.blit(splash, (0,0))
            pygame.display.update()
            pygame.time.wait(100)

        pygame.mixer.fadeout(2000)
        screen.blit( splash,(0,0) )
        pygame.display.update()
        pygame.time.wait(1500)

        screen.fill( (255,255,255) )    # clean up by erasing the background to normal white

        self.ops.func_main_menu()


    def setup(self):
        self.ops.func_main_menu.append( self.func_main_menu )
        self.ops.func_splash_screen.append( self.func_splash_screen )

        sp = self.maker.make_splash( self.ops.func_splash_screen, {"screen":None} )
        self.map.objects_splash_screen["starter"] = sp
