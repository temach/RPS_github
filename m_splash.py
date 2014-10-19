#! /usr/bin/env python-32
# -*- coding: utf-8 -*-

import os.path
import pygame
#import pygame.locals as PL

import util
from elements import ElementBase
import resources
import random


def myrandom(n):
    # another layer of overhead...
    return random.randrange(n)

class Meltdown:
    def __init__(self, surface, min_size=90, max_size=100, min_dist=50,
            min_width=30, width_add=20, finished=50):
        """
        min_size=10,
        max_size=100,
        min_dist=10,
        min_width=30,
        width_add=20,
        finished=50
        """


        self.surf = surface

        self.WIDTH, self.HEIGHT = surface.get_size()

        self.MIN_SIZE = min_size
        self.MAX_SIZE = max_size

        self.MIN_DIST = min_dist

        self.MIN_WIDTH = min_width
        self.WIDTH_ADD = width_add

        self.MAX_HEIGHT = self.HEIGHT - self.MIN_SIZE
        self.FINISHED = finished

        self.heights = []
        while len(self.heights) < self.WIDTH: self.heights.append(0)

        self.finished = 0


    def step(self):
        # redefinitions to speed things up a little bit
        WIDTH = self.WIDTH
        MIN_WIDTH = self.MIN_WIDTH
        HEIGHT = self.HEIGHT
        MAX_HEIGHT = self.MAX_HEIGHT

        rand = myrandom
        heights = self.heights
        surf = self.surf

        _range = range
        _min = min
        _max = max

        # precalculations
        width = rand(MIN_WIDTH) + self.WIDTH_ADD

        #xloc = self.calc_xloc(width)
        xloc = rand(WIDTH + MIN_WIDTH) - 2*MIN_WIDTH
        xloc = _max(_min((xloc + width), (WIDTH - width)), 0)

        yloc = HEIGHT
        for i in _range(xloc, (xloc + width)):
            yloc = _min(yloc, heights[i])
        if yloc == HEIGHT:
            return surf, []

        # calculate block size
        dist = rand(yloc/10 + self.MIN_DIST)
        size = rand(_max(yloc + self.MIN_SIZE, self.MAX_SIZE))

        # define rects for blitting
        destpos = (xloc, yloc + dist)
        destrect = (xloc, yloc, width, dist)
        sourcerect = (xloc, yloc, width, size)

        # the visible bit
        surf.blit(surf, destpos, sourcerect)
        surf.fill((0, 0, 0), destrect)

        # postcalculations
        yloc += dist
        for i in _range(xloc, (xloc + width)):
            if heights[i] < MAX_HEIGHT and yloc >= MAX_HEIGHT:
                self.finished += 1
            heights[i] = _max(heights[i], yloc)

        if self.finished >= (WIDTH - self.FINISHED):
            return None, []

        # everything is fine, return the new surface
        return surf, [sourcerect, destrect]


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


    def func_splash_screen(self, func_vars=None):       # entry point
        """
        Show the splash screen.
        This is called once when the game is first started.
        """
        screen = func_vars["screen"]

        pygame.mixer.music.load( self.music_path )
        pygame.mixer.music.play()

        splash = pygame.image.load( self.image_path ).convert()
        splash = pygame.transform.smoothscale( splash, (800,600) )

        # blit the surface to the screen
        screen.blit(splash, (0,0))
        pygame.display.flip()

        # instantiate the Meltdown class
        meltdown = Meltdown( splash )

        # first step
        surface, dirty = meltdown.step()

        # main loop
        while surface:
            pygame.event.pump()     # tell OS that we are processing the events and are not simply frozen.

            #surface, dirty = meltdown.step()

            # redraw screen
            screen.blit( surface, (0,0))
            pygame.display.update( dirty )

            # next step
            surface, dirty = meltdown.step()


        pygame.mixer.fadeout(2000)
        screen.blit( splash,(0,0) )
        pygame.display.update()
        pygame.time.wait(1500)

        screen.fill( (255,255,255) )    # clean up by erasing the background to normal white

        self.active.unbind( self.map.objects_splash_screen )
        self.ops.func_main_menu()


    def setup(self):
        #self.ops.func_main_menu.append( self.func_main_menu )
        self.ops.func_splash_screen.append( self.func_splash_screen )

        sp = self.maker.make_splash( self.ops.func_splash_screen, {"screen":None} )
        self.map.objects_splash_screen["starter"] = sp
