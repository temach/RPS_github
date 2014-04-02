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
    """
    program level function: function is added to function group. this means that its
    instructions affect more than one module, so its code should make sense
    without understanding the context in which it was invoked AND code
    should be encapsulated since the function can be called from anywhere
    at anytime.

    module level function: function is used within the module. this means that its
    instructions (and its effect on the user) make sense when other parts
    of the same module are active.


    This class is a list of program level functions. On registration different
    modules ( this look like "m_MODULENAME.py" ) add functions to these
    lists.
    This allows buttons to alert multiple objects of changes by calling
    a FunctionsGroup object as if it was a standart function.
    Basically when a user clicks a button, many things need to change. But
    a button can only call one function. Hence I decided to make this one
    function a list of functions. This way with a single call an arbitrary
    number of functions can execute. This makes adding and/or removing
    functionality to the overall program very straight forward.

    Say when you press a button music starts to play and you want to
    remove that. You find the name of the FunctionGroup that is the last
    executed before music plays. You should then look through all of
    the modules ( m_MODULENAME.py files ) that can be connected to either
    the button or the music. A number of them will have a function called the
    same as the FunctionsGroup. Look inside all of those functions and find
    the one that is causing the sound.
    """

    REFRESH = PL.USEREVENT + 1
    REFRESHEVENT = pygame.event.Event(REFRESH, info="Send an event to pygame.event.wait to refresh the screen")

    def __call__(self, func_vars=None):
        for func in self:
            func( func_vars )

        pygame.event.post( self.REFRESHEVENT )


        # START DEBUG
        text = "Calling FunctionsGroup: {name} \n \t"
        text = text + "\n \t".join( ( repr(func.im_class)[8:~1] for func in self ) )
        if func:            # if the FunctionsGroup contains at least one function, this variable will not be None.
            text = text.format( name=func.__name__ )       # use the last func variable to get the name of the FunctionsGroup
        print text
        # END DEBUG


