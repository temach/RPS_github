import pickle
import pygame
import pygame.locals as PL

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
        return None # happens if high_scores.txt file is completely empty. (When run for the first time)   EOFError = End Of File Error


def write_pickle_file( filepath, data ):
    with open( filepath, 'wb') as datafile:
        pickle.dump( data, datafile )




class FunctionsGroup( list ):
    REFRESH = PL.USEREVENT + 1
    REFRESHEVENT = pygame.event.Event(REFRESH, info="Send an event to pygame.event.wait to refresh the screen")

    def __call__(self, func_vars=None):
        for func in self:
            func( func_vars )

        pygame.event.post( self.REFRESHEVENT )

