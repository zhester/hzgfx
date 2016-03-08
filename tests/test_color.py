#=============================================================================
#
# color Module Unit Tests
#
#=============================================================================

"""
color Module Unit Tests
=======================
"""


import unittest

import hzgfx.color


#=============================================================================
class ColorTests( unittest.TestCase ):
    """
    Tests the color module
    """


    #=========================================================================
    def test_set( self ):
        """
        Tests setting color values from various types/formats.
        """

        # color in a dictionary
        dc = { 'r' : 99, 'g' : 88, 'b' : 77 }

        # color in an object
        class CObj( object ):
            r = 66
            g = 55
            b = 44
        co = CObj()

        # color in a non-list or non-tuple sequence
        class CSeq( object ):
            def __getitem__( self, i ):
                return 0x33
            def __len__( self ):
                return 3
        cs = CSeq()

        # test cases as: input, expected integer, expected tuple
        cases = [
            (          0, 0x000000, (    0,    0,    0 ) ),
            (          1, 0x000001, (    0,    0,    1 ) ),
            (        256, 0x000100, (    0,    1,    0 ) ),
            (      65536, 0x010000, (    1,    0,    0 ) ),
            (   0xFFFFFF, 0xFFFFFF, (  255,  255,  255 ) ),
            (  '#000000', 0x000000, (    0,    0,    0 ) ),
            (  '#FFFFFF', 0xFFFFFF, (  255,  255,  255 ) ),
            (      'F07', 0xFF0077, (  255,    0, 0x77 ) ),
            ( '0x112233', 0x112233, ( 0x11, 0x22, 0x33 ) ),
            (         dc, 0x63584D, (   99,   88,   77 ) ),
            (         co, 0x42372C, (   66,   55,   44 ) ),
            (         cs, 0x333333, (   51,   51,   51 ) )
        ]

        # set up a Color object under test
        c = hzgfx.color.Color()

        # run each test case
        for case in cases:
            c.set( case[ 0 ] )
            self.assertEqual( case[ 1 ], c._int, msg = str( case[ 0 ] ) )
            self.assertEqual( case[ 2 ], c._rgb, msg = str( case[ 0 ] ) )

