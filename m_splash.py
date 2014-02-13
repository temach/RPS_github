#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import time
import pygame
import pygame.locals as PL
pygame.init()

import constants
import resources

import os



class Splash( pygame.sprite.Sprite ):
    def __init__(self, func_to_call, func_vars):
        pygame.sprite.Sprite.__init__(self)

        self.id = id(self)
        self.rect = pygame.Rect(0,0,0,0)
        self.func = func_to_call
        self.func_vars = func_vars
        self.has_run = False
        self.screen = None

    def receive_event(self, event):
        return

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



class MakerLocal(object):

    def make_splash(self, func_to_call, func_vars):
        sp = Splash( func_to_call, func_vars )
        return sp






class SplashModule(object):
    def __init__(self, active, operators, mapper):
        self.active = active
        self.ops = operators
        self.map = mapper

        self.maker = MakerLocal()

        self.music_path = os.path.join("data", "splash.ogg")
        self.image_path = os.path.join("data", "gimpysplash.png")


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

        for i in range(27):
            pygame.event.pump()     # otherwise OS thinks the app is frozen
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
        self.ops.func_groups["main_menu"].append( self.func_main_menu )
        self.ops.func_groups["splash_screen"].append( self.func_splash_screen )

        sp = self.maker.make_splash( self.ops.func_splash_screen, {"screen":None} )
        self.map.objects_splash_screen["starter"] = sp









if __name__=="__main__":

    import pygame
    import pygame.locals as PL
    import time
    from sys import exit

    from util import debug      # Use as decorator. So put "@debug" just before function definition.
    from util import ActiveGroup


    class Operator(object):     # The operator describes what functions there are, in your files you describe how they work.
        def __init__(self):

            self.func_groups = {        # { function_name:[ list of functions to execute ], ....
                "main_menu":[],
                "splash_screen":[],
            }

        def func_main_menu(self, func_vars=None):
            for function in self.func_groups["main_menu"]:
                function( func_vars )      # run/execute the function

        def func_splash_screen(self, func_vars=None):
            for function in self.func_groups["splash_screen"]:
                function( func_vars )      # run/execute the function




    class Mapper(object):      # Describes what options you have. In your files you describe how these dictionaries look, the Mapper describes what dictionaries there are.
        def __init__(self):
            self.objects_menu = {}
            self.objects_splash_screen = {}



    pygame.init()

    screen = pygame.display.set_mode( (800,600) )


    operators = Operator()
    mapper = Mapper()
    active = ActiveGroup()

    clock = pygame.time.Clock()


    # Here enter the name of the module
    module = SplashModule( active, operators, mapper )
    module.setup()

    active.bind( mapper.objects_splash_screen )


    screen.fill((200,200,240))
    legal_events = (PL.KEYDOWN, PL.KEYUP, PL.MOUSEMOTION, PL.MOUSEBUTTONUP, PL.MOUSEBUTTONDOWN)
    keyboard_events =(PL.KEYDOWN, PL.KEYUP)



    while True:
        event = pygame.event.wait()

        if event.type==PL.QUIT or ( (event.type in keyboard_events) and (event.key == PL.K_q or event.key==PL.K_ESCAPE) ):
            exit()

        elif event.type in legal_events:
            active.manage_event( event )

        #active.clear(screen, background)

        dirty_rects = active.manage_render( screen )
        pygame.display.update(dirty_rects)

        active.manage_run()

        clock.tick(17)



