if __name__=="__main__":

    import pygame
    import pygame.locals as PL
    import time
    from sys import exit

    from util import debug      # Use as decorator. So put "@debug" just before function definition.
    from util import ActiveGroup
    from util import FunctionsGroup


    class Operator(object):     # The operator describes what functions there are, in your files you describe how they work.
        def __init__(self):
            self.func_main_menu = FunctionsGroup()
            self.func_game = FunctionsGroup()
            self.func_view_scores = FunctionsGroup()
            self.func_credits = FunctionsGroup()


    class Mapper(object):      # Describes what options you have. In your files you describe how these dictionaries look, the Mapper describes what dictionaries there are.
        def __init__(self):
            self.objects_menu = {}



    pygame.init()

    screen = pygame.display.set_mode( (800,600) )


    operators = Operator()
    mapper = Mapper()
    active = ActiveGroup()

    clock = pygame.time.Clock()


    # Here enter the name of the module
    module = MainMenuModule( active, operators, mapper )
    module.setup()

    active.bind( mapper.objects_menu )



    background = pygame.Surface( screen.get_size() )
    background.fill( (240,240,240) )

    screen.blit( background, (0,0))
    pygame.display.flip()


    legal_events = (PL.KEYDOWN, PL.KEYUP, PL.MOUSEMOTION, PL.MOUSEBUTTONUP, PL.MOUSEBUTTONDOWN)
    keyboard_events =(PL.KEYDOWN, PL.KEYUP)


    while True:
        event = pygame.event.wait()

        if event.type==PL.QUIT or ( (event.type in keyboard_events) and (event.key == PL.K_q or event.key==PL.K_ESCAPE) ):
            exit()

        elif event.type in legal_events:
            active.manage_event( event )

        active.clear(screen, background)

        dirty_rects = active.manage_render( screen )
        pygame.display.update(dirty_rects)

        active.manage_run()

        clock.tick(20)
