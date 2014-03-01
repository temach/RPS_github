import pygame
import os
from elements import Button, Reader



class MakerBasic( object ):

    def get_surfaces(self, path, rect=False):
        img_types = ("_out.png", "_over.png", "_down.png")
        all_imgs = ( pygame.image.load( path + extra ).convert()  for extra in img_types )

        if rect: all_imgs = ( pygame.transform.smoothscale(surf, rect.size) for surf in all_imgs )

        return all_imgs


    def make_button(self, rect, func_to_call, img_name, func_vars=None, rescale=False):
        img_reference = os.path.join( "img", img_name)

        surf_list = (rescale and self.get_surfaces( img_reference, rect)) or self.get_surfaces( img_reference )
        # Above trick: google for "python and/or trick to select values inline"

        b = Button( surf_list, rect, func_to_call, func_vars)
        return b


    def make_reader(self, text, pos, width, style_name):
        """ text, pos and width are necessary. """
        if not type(text)==unicode:
            text = unicode(text.expandtabs(4), 'utf8')

        style_reader1 = {
            "fontsize": 17,
            "font": "mono",
            "height": 380,
            "bgcolor": (150,150,150,0),
            "fgcolor": (0,0,0,0),           # text color
            "hlcolor": (180,180,200,0),      # highlighted text color
            "split": True,                  # wrap lines automatically
        }

        t = Reader( text, pos, width, style_reader1)
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
        try:           # presume that it is a dictionary
            self.add(  *getattr(stuff, "values", None)()  )
        except TypeError:       # its not a dict, then it must be an iterable.
            self.add( *stuff )

    def unbind(self, stuff=None, *args, **kwargs):
        """remove(sprite, list, or group, ...)
           remove sprite from group
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
        #print len(self.sprites())
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
