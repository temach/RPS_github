import pygame


def debug( func_to_wrap ):

    def print_arguments_wrapper( *args ):       # this wrapped prints the arguments to the function
        print
        print
        print "debug: Function __{0}__   got args:    {1} ".format(func_to_wrap.__name__, args)
        func_to_wrap( *args )

    return print_arguments_wrapper



class FunctionsGroup( list ):
    def __call__(self, func_vars=None):
        for func in self:
            func( func_vars )



class ActiveGroup( pygame.sprite.RenderUpdates ):

    def add(self, *sprites):
        """add sprite to group
           This is an inside method. Call .bind() to bind/add to group
           Add a sprite or sequence of sprites to a group."""
        for sprite in sprites:
            if not self.has_internal(sprite):
                self.add_internal(sprite)
                sprite.add_internal(self)

    def remove(self, *sprites):
        """remove sprite from group
           This is an inside method. Call .unbind() to unbind/remove to group
           Remove a sprite or sequence of sprites from a group."""
        for sprite in sprites:
            if self.has_internal(sprite):
                self.remove_internal(sprite)
                sprite.remove_internal(self)




    def bind(self, stuff=None, *args, **kwargs):
        """add(sprite, list, or group, ...)
           add sprite to group
           Add a sprite or sequence of sprites to a group."""

        try:            # presume that it is a dictionary
            if args: print "The first argument is an iterable, hence all other args except for keywords are ignored. Consider adding them to the first iterable."
            self.add( *stuff.values() )
        except AttributeError:       # its not a dict, but its most probably an iterable.
            try:
                if args: print "The first argument is an iterable, hence all other args except for keywords are ignored. Consider adding them to the first iterable."
                self.add( *stuff )
            except TypeError:           # ok, so "stuff" is not an iterable, its just one object, then any args passed after can also be only objects
               self.add( stuff, *args )


    def unbind(self, stuff=None, *args, **kwargs):
        """add(sprite, list, or group, ...)
           add sprite to group
           Add a sprite or sequence of sprites to a group."""

        try:            # presume that it is a dictionary
            if args: print "The first argument is an iterable, hence all other args except for keywords are ignored. Consider adding them to the first iterable."
            self.remove( *stuff.values() )
        except AttributeError:       # its not a dict, but its most probably an iterable.
            try:
                if args: print "The first argument is an iterable, hence all other args except for keywords are ignored. Consider adding them to the first iterable."
                self.remove( *stuff )
            except TypeError:           # ok, so "stuff" is not an iterable, its just one object, then any args passed after can also be only objects
               self.remove( stuff, *args )


    def manage_event(self, *args):
        """receive_event(*args)
           spread information for all member sprites.
           this is the first step of the update process."""
        for s in self.sprites(): s.receive_event(*args)


    def manage_run(self, *args):
        """run(*args)
            the *args should normally be empty.
            If you want to pass something use receive_event( something )
            call run for all member sprites, so they can act on info received.
            this is the second step of the update process."""
        for s in self.sprites(): s.run(*args)


    def manage_render(self, surface):
        """
        Calls sprite.render( surface ) on all sprites in Group.
        sprite.render( surface ) is supposed to return a pygame.Rect to update.
        """
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append

        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = spr.render( surface )      #  .render() should return a rectangle to update.
            if rec is 0:                     # TODO: I think I can get rid of this "if rec is 0:" check.
                dirty_append( newrect )
            else:
                if newrect.colliderect(rec):
                    dirty_append( newrect.union(rec) )
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty
