import pygame


def debug( func_to_wrap ):

    def print_arguments_wrapper( *args ):       # this wrapped prints the arguments to the function
        print
        print
        print "debug: Function __{0}__   got args:    {1} ".format(func_to_wrap.__name__, args)
        func_to_wrap( *args )

    return print_arguments_wrapper


def read_pickle_file( filepath ):
    try:
        with open( filepath, 'rb') as datafile:
            return pickle.load( datafile )
    except EOFError:
        return {} # happens when run for the first time. Because the high_scores.txt file is completely empty.    EOFError = End Of File Error

    except Exception as exc:
        print("Got Error:  {0} {1}".format( type(exc), exc.args))
        raise






class FunctionsGroup( list ):
    def __call__(self, func_vars=None):
        for func in self:
            func( func_vars )




class MakerBasic( object ):

    def get_surfaces(self, path, rect=False):
        img_types = ("_out.png", "_over.png", "_down.png")
        all_imgs = ( pygame.image.load( path + extra ).convert()  for extra in img_types )

        if rect: all_imgs = ( pygame.transform.smoothscale(surf, rect.size) for surf in all_imgs )

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



    def make_form(self, pos, width, **kws):
        """
        Creates a form, but remember that a form's input can not be grabbed without a form confirmation button

        """
        f = Form( pos, width, kws.get("fontsize", 12),
                                kws.get("height", 12),
                                kws.get("font", 12),
                                kws.get("bg", 12),
                                kws.get("fgcolor", 12),
                                kws.get("hlcolor", 12),
                                kws.get("curscolor", 12),
                                kws.get("maxlines", 0) )
        return f



    def make_form_prompter(self, some_form, rect, func_to_call, img_name="confirm", rescale=False):
        surf_list = self.get_surfaces( img_reference, rect) if rescale else self.get_surfaces( img_reference )

        fm = FormPrompter( surf_list, rect, func_to_call, {"user_input":""}, some_form )    # the "some_form" here referes to any Form that would be used to grab the user's input
        return fm









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
