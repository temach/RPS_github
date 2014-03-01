import pickle


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

