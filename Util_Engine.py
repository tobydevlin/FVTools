
# Function to take in a depth-averaging reference and return
# an interface to the C++-Library that will run this
def get_dave_fun(ref):
    from numpy.ctypeslib import ndpointer
    import ctypes as ct
    
    davelib=ct.CDLL(r'Release\Util_Engine.dll')

    float_arg = [ndpointer(ct.c_float, flags="C_CONTIGUOUS"),
                 ndpointer(ct.c_float, flags="C_CONTIGUOUS"),
                 ndpointer(ct.c_int32, flags="C_CONTIGUOUS"),
                 ndpointer(ct.c_int32, flags="C_CONTIGUOUS"),
                 ct.c_float,ct.c_float,
                 ndpointer(ct.c_float, flags="C_CONTIGUOUS"),
                 ct.c_int32]
    integ_arg = [ndpointer(ct.c_float, flags="C_CONTIGUOUS"),
                 ndpointer(ct.c_float, flags="C_CONTIGUOUS"),
                 ndpointer(ct.c_int32, flags="C_CONTIGUOUS"),
                 ndpointer(ct.c_int32, flags="C_CONTIGUOUS"),
                 ct.c_int32,ct.c_int32,
                 ndpointer(ct.c_float, flags="C_CONTIGUOUS"),
                 ct.c_int32]

    if ref=='sigma':
        dave_fun = davelib.dave_sig
        dave_fun.restype = None
        dave_fun.argtypes = float_arg
    elif ref=='height':
        dave_fun = davelib.dave_height
        dave_fun.restype=None
        dave_fun.argtypes = float_arg
    elif ref=='depth':
        dave_fun = davelib.dave_depth
        dave_fun.restype=None
        dave_fun.argtypes = float_arg
    elif ref=='elevation':
        dave_fun = davelib.dave_elevation
        dave_fun.restype=None
        dave_fun.argtypes = float_arg
    elif ref=='top':
        dave_fun = davelib.dave_top
        dave_fun.restype=None
        dave_fun.argtypes = integ_arg
    elif ref=='bot':
        dave_fun = davelib.dave_bottom
        dave_fun.restype=None
        dave_fun.argtypes = integ_arg

    return dave_fun
    
    
# Maybe have other function interfaces.
