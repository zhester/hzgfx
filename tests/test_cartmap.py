#=============================================================================
#
# cartmap Module Unit Tests
#
#=============================================================================

"""
cartmap Module Unit Tests
=========================
"""


import unittest

import hzgfx.cartmap


#=============================================================================
class TestAxis( unittest.TestCase ):
    """
    Tests the Axis class.
    """


    #=========================================================================
    def test_init( self ):
        """
        Tests the __init__ method.
        """

        # Width-specified, integer axis
        axis = hzgfx.cartmap.Axis( 10 )
        self.assertEqual( 0, axis.start )
        self.assertEqual( 10, axis.stop )
        self.assertEqual( 1, axis.step )
        self.assertIs( axis.type, int )

        # Extreme-specified, integer axis
        axis = hzgfx.cartmap.Axis( 3, 8 )
        self.assertEqual( 3, axis.start )
        self.assertEqual( 8, axis.stop )
        self.assertEqual( 1, axis.step )
        self.assertIs( axis.type, int )

        # Extreme-specified, integer axis, with alternate step
        axis = hzgfx.cartmap.Axis( 0, 4, 2 )
        self.assertEqual( 0, axis.start )
        self.assertEqual( 4, axis.stop )
        self.assertEqual( 2, axis.step )
        self.assertIs( axis.type, int )

        # Width-specified, float axis
        axis = hzgfx.cartmap.Axis( 1.0 )
        self.assertEqual( 0.0, axis.start )
        self.assertEqual( 1.0, axis.stop )
        self.assertEqual( 1.0, axis.step )
        self.assertIs( axis.type, float )

        # Extreme-specified, float axis
        axis = hzgfx.cartmap.Axis( 3.5, 8.2 )
        self.assertAlmostEqual( 3.5, axis.start )
        self.assertAlmostEqual( 8.2, axis.stop )
        self.assertEqual( 1.0, axis.step )
        self.assertIs( axis.type, float )

        # Extreme-specified, float axis, with alternate step
        axis = hzgfx.cartmap.Axis( 0.0, 0.4, 0.2 )
        self.assertAlmostEqual( 0.0, axis.start )
        self.assertAlmostEqual( 0.4, axis.stop )
        self.assertAlmostEqual( 0.2, axis.step )
        self.assertIs( axis.type, float )


    #=========================================================================
    def test_len( self ):
        """
        Tests the __len__ method.
        """

        # Integer axes
        axis = hzgfx.cartmap.Axis( 10 )
        self.assertEqual( 10, len( axis ) )
        axis = hzgfx.cartmap.Axis( 0, 8 )
        self.assertEqual( 8, len( axis ) )
        axis = hzgfx.cartmap.Axis( 0, 8, 2 )
        self.assertEqual( 4, len( axis ) )
        axis = hzgfx.cartmap.Axis( 0, 7, 2 )
        self.assertEqual( 3, len( axis ) )

        # Float axes
        axis = hzgfx.cartmap.Axis( 2.0 )
        self.assertEqual( 2, len( axis ) )
        axis = hzgfx.cartmap.Axis( 5.0, 9.0 )
        self.assertEqual( 4, len( axis ) )
        axis = hzgfx.cartmap.Axis( 0.2, 0.8, 0.2 )
        self.assertEqual( 3, len( axis ) )
        axis = hzgfx.cartmap.Axis( 0.2, 0.7, 0.2 )
        self.assertEqual( 2, len( axis ) )


    #=========================================================================
    def test_str( self ):
        """
        Tests the __str__ method.
        """
        axis = hzgfx.cartmap.Axis( 0, 8, 2 )
        self.assertEqual( '[0:8:2]', str( axis ) )
        axis = hzgfx.cartmap.Axis( -3.1, 8.3, 0.5 )
        self.assertEqual( '[-3.1:8.3:0.5]', str( axis ) )


    #=========================================================================
    def test_delta( self ):
        """
        Tests the delta method.
        """
        axis = hzgfx.cartmap.Axis( 0, 8, 2 )
        self.assertEqual( 8, axis.delta() )
        axis = hzgfx.cartmap.Axis( -3.1, 8.3, 0.5 )
        self.assertAlmostEqual( 11.4, axis.delta() )


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main() 

