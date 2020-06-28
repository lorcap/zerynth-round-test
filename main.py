# divmod from Zerynth
#
# This is file is meant to be run through both Zerynth and Python3
# as to compare the two implementations.
#
# The obvious thing to do when rounding floats is:
#
#   round(n * 10**ndigits, None) / 10**ndigits
#
# Because these extra operations can reduce precision of the result,
# Python fiddles with a double converted to a string
# (see https://stackoverflow.com/a/56987434/811724).
#
# These two approaches lead to different results.

try:
    # works in Zerynth
    import streams
    streams.serial()

    sys_round = __builtins__.round

except:
#-if False
    # works in Python
    pyround = round

    def round(number, ndigits=None):
        if ndigits == None:
            return pyround(number)
        elif type(ndigits) is int:
            r = pyround(number * 10**ndigits)/10**ndigits
            return r if type(number) == float else int(r)
        else:
            raise TypeError
#-endif
    pass

###########################################################

fmt = '%05s'
def test(a, b, exp, epy=None):
    got = round(a,b)
    got_str = fmt % str(got)
    exp_str = fmt % str(exp)
    print('round(%05s, %04s) ' % (str(a), str(b)), end='')
    if exp_str == got_str:
        print('== %s (pass)' % exp_str, end='')
        if epy != None:
            pyr_str = fmt % epy
            print(' (Python: %s)' % pyr_str, end='')
#-if False
        pyr_str = fmt % pyround(a,b)
        if (epy == None and pyr_str != exp_str) or\
           (epy != None and pyr_str != fmt % epy):
                print('\n  Python: %s' % pyr_str, end='')
#-endif
        print()
    else:
        print('fail\n  expected: %s\n  got: %s' % (exp, got))

###########################################################

try:
    test(  0    , None,   '0'   )
    test(  0.1  , None,   '0'   )
    test(  0.5  , None,   '0'   )
    test(  0.6  , None,   '1'   )
    test(  1    , None,   '1'   )
    test(  1.1  , None,   '1'   )
    test(  1.5  , None,   '2'   )
    test(  1.6  , None,   '2'   )
    test(  2.5  , None,   '2'   )
    test(  3.5  , None,   '4'   )

    test( -0.1  , None,   '0'   )
    test( -0.5  , None,   '0'   )
    test( -0.6  , None,  '-1'   )
    test( -1    , None,  '-1'   )
    test( -1.1  , None,  '-1'   )
    test( -1.5  , None,  '-2'   )
    test( -1.6  , None,  '-2'   )
    test( -2.5  , None,  '-2'   )
    test( -3.5  , None,  '-4'   )

    test(  0    ,    2,   '0'   )
    test(  0.001,    2,   '0.0' )
    test(  0.005,    2,   '0.0' , '0.01')
    test(  0.015,    2,   '0.02', '0.01')
    test(  0.025,    2,   '0.02', '0.03')
    test(  0.105,    2,   '0.1' )
    test(  0.006,    2,   '0.01')
    test(  1.0  ,    2,   '1.0' )
    test(  1.111,    2,   '1.11')
    test(  1.115,    2,   '1.12', '1.11')
    test(  1.125,    2,   '1.12')
    test(  1.116,    2,   '1.12')
    test(  2.675,    2,   '2.68', '2.67')

    test(  0    ,    0,   '0'   )
    test(  0.001,    0,   '0.0' )
    test(  0.005,    0,   '0.0' )
    test(  0.015,    0,   '0.0' )
    test(  0.025,    0,   '0.0' )
    test(  0.105,    0,   '0.0' )
    test(  0.006,    0,   '0.0' )
    test(  1.0  ,    0,   '1.0' )
    test(  1.111,    0,   '1.0' )
    test(  1.115,    0,   '1.0' )
    test(  1.125,    0,   '1.0' )
    test(  1.116,    0,   '1.0' )
    test(  2.675,    0,   '3.0' )

    test(  0    ,   -2,   '0'   )
    test( 10    ,   -2,   '0'   )
    test( 50    ,   -2,   '0'   )
    test( 60    ,   -2, '100'   )
    test(  1.0  ,   -2,   '0.0' )
    test(110.0  ,   -2, '100.0' )
    test(150    ,   -2, '200'   )
    test(160.0  ,   -2, '200.0' )

except Exception as e:
#-if False
    raise
#-endif
    print("Something bad happened:",e)
