import pygame
import os

from elements import Button, Reader, Form, FormPrompter
import styles
import resources


class ModuleBasic( object ):

    def setup(self):
        return

    def debug_setup(self):
        """Use this to define the infrastructure that will be needed for the
        module to function. In other words define the objects which affect
        the module's initial entering and/or exiting conditions. Things that
        surround this module, but are also implemented elsewhere. Call this function
        when you want to test one module in isolation.
        """
        return


class StyleLoader( object ):
    resources.set_images_path( "img" )
    resources.set_sounds_path( "sound" )


    def get_button_surfaces(self, img_name, size=False):
        assert (type( size )==tuple) or (size is False), "Arg 'size' is not the right type! Maybe its a pygame.Rect?"
        assert ("." not in img_name) and type(img_name)==str, "You have a '.' in the image name stated in 'styles.py': " + str(img_name) + "  \nThis should be image for a button. Please remove the '.' character (and/or the image extension) in the 'styles.py' file."

        img_types = ("_out.png", "_over.png", "_down.png")
        all_imgs = ( resources.get_image( img_name + extra ) for extra in img_types )

        # if size if False, return unmodified imgs, else return a generator of modified imgs.
        return all_imgs #if (not size) else ( pygame.transform.smoothscale(surf, size) for surf in all_imgs )


    def get_form_surfaces( self, img_name ):
        img_types = ("_off.png", "_on.png" )
        all_imgs = ( resources.get_image( img_name + extra ) for extra in img_types )
        return all_imgs


    def get_img(self, img_name, size=False):
        surf = resources.get_image( img_name )
        return surf if (not size) else pygame.transform.smoothscale(surf, size)

    def change_menu_imgs(self):
        resources.get_image("menu_over.png", True)


class MakerBasic( StyleLoader ):


    def make_button(self, pos, style_name, func_to_call, func_vars=None, rescale=True):
        assert getattr( styles, style_name, False ), "Module 'style.py' has no style dictionary called " + str(style_name) + " . Check your spelling."
        assert type( pos )==tuple, "Variable 'pos' has strange type. Should be a tuple of (x,y)."
        assert (type( func_vars )==dict) or (func_vars is None), "Variable 'func_vars' has strange type. Should be a dictionary."

        style_dict = getattr( styles, style_name )

        surf_list = self.get_button_surfaces( style_dict["img"], style_dict["size"] ) if rescale else self.get_button_surfaces( style_dict["img"] )
        rect = pygame.Rect( pos, style_dict["size"] )

        b = Button( surf_list, rect, func_to_call, func_vars)

        print "make_button() ", self.__module__, self
        return b


    def make_reader(self, text, pos, width, style_name):
        """ text, pos and width are necessary. """
        assert getattr( styles, style_name, False ), "Module 'style.py' has no style dictionary called  {0}\n Check your spelling.".format( style_name )

        if not type(text)==unicode:
            text = unicode(text.expandtabs(4), 'utf8')

        style_dict = getattr( styles, style_name )
        t = Reader( text, pos, width, style_dict)
        return t


    def make_form(self, pos, style_name):
        """ Creates a form, but remember that a form's input can not be grabbed without a form confirmation button"""

        style_dict = getattr( styles, style_name, False ) or {}
        try:
            style_dict["bgimgs"] = self.get_form_surfaces( style_dict["img"] )
        except KeyError:
            style_dict["bgimgs"] = (None, None)
        f = Form( pos, style_dict["width"], style_dict)
        return f



    def make_form_prompter(self, some_form, rect, func_to_call, img_name="confirm", rescale=False):
        surf_list = self.get_button_surfaces( img_name ) #if (not rescale) else self.get_button_surfaces( img_name, rect.size )

        fm = FormPrompter( surf_list, rect, func_to_call, {"user_input":""}, some_form )    # the "some_form" here referes to any Form that would be used to grab the user's input
        return fm







class ActiveGroup( pygame.sprite.RenderUpdates ):

    def add(self, *sprites):
        """This is an inside method. Call .bind() to bind/add to group
           Add a sprite or sequence of sprites to a group."""
        for sprite in sprites:
            if not self.has_internal(sprite):
                self.add_internal(sprite)
                sprite.add_internal(self)

    def remove(self, *sprites):
        """This is an inside method. Call .unbind() to unbind/remove to group
           Remove a sprite or sequence of sprites from a group."""
        for sprite in sprites:
            if self.has_internal(sprite):
                self.remove_internal(sprite)
                sprite.remove_internal(self)



    def bind(self, stuff=None, **kwargs):
        """add(sprite, list, or group, ...)
           Add a sprite or sequence of sprites to a group."""
        try:           # presume that it is a dictionary
            self.add(  *getattr(stuff, "values", None)()  )
        except TypeError:       # its not a dict, then it must be an iterable.
            self.add( *stuff )

    def unbind(self, stuff=None, **kwargs):
        """remove(sprite, list, or group, ...)
           remove a sprite or sequence of sprites from a group."""
        try:           # presume that it is a dictionary
            self.remove(  *getattr(stuff, "values", None)()  )
        except TypeError:       # its not a dict, then it must be an iterable.
            self.remove( *stuff )



    def manage_event(self, *args):
        """spread information for all member sprites.
           this is the first step of the update process."""
        for s in self.sprites(): s.receive_event(*args)

    def manage_run(self, *args):
        """the *args should normally be empty.
            If you want to pass something use receive_event( something )
            call run for all member sprites, so they can act on info received.
            this is the second step of the update process."""
        for s in self.sprites(): s.run(*args)

    def manage_render(self, surface):
        """Calls sprite.render( surface ) on all sprites in Group.
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

















"""

    def make_form(self, pos, width, **kws):
        #Creates a form, but remember that a form's input can not be grabbed without a form confirmation button

        f = Form( pos, width, kws.get("fontsize", 12),
                                kws.get("height", 12),
                                kws.get("font", None),
                                kws.get("bg", None),
                                kws.get("fgcolor", 12),
                                kws.get("hlcolor", 12),
                                kws.get("curscolor", 12),
                                kws.get("maxlines", 0) )
        return f



"""
