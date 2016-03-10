#=============================================================================
#
# interval Module Unit Tests
#
#=============================================================================

"""
interval Module Unit Tests
==========================
"""


import unittest

import hzgfx.interval


#=============================================================================
class Testinterval( unittest.TestCase ):
    """
    Tests the interval function.
    """


    #=========================================================================
    def test_interval( self ):

        # All default interval.
        interval = hzgfx.interval.interval()
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 0.0, interval.start )
        self.assertEqual( 1.0, interval.stop )
        self.assertEqual( 1.0, interval.step )

        # All default interval.
        interval = hzgfx.interval.interval( None )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 0.0, interval.start )
        self.assertEqual( 1.0, interval.stop )
        self.assertEqual( 1.0, interval.step )

        # Simple size interval.
        interval = hzgfx.interval.interval( 10 )
        self.assertIsInstance( interval, hzgfx.interval.Interval )
        self.assertEqual( 0, interval.start )
        self.assertEqual( 10, interval.stop )
        self.assertEqual( 1, interval.step )

        # Complete size interval.
        interval = hzgfx.interval.interval( 1, 7, 3 )
        self.assertIsInstance( interval, hzgfx.interval.Interval )
        self.assertEqual( 1, interval.start )
        self.assertEqual( 7, interval.stop )
        self.assertEqual( 3, interval.step )

        # Simple continuous interval.
        interval = hzgfx.interval.interval( 3.0 )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 0.0, interval.start )
        self.assertEqual( 3.0, interval.stop )
        self.assertEqual( 1, interval.step )

        # Complete continuous interval.
        interval = hzgfx.interval.interval( -7.0, 7.0, 0.5 )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( -7.0, interval.start )
        self.assertEqual( 7.0, interval.stop )
        self.assertEqual( 0.5, interval.step )

        # Tuple arguments (1).
        interval = hzgfx.interval.interval( ( 2.0, ) )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 0.0, interval.start )
        self.assertEqual( 2.0, interval.stop )
        self.assertEqual( 1, interval.step )

        # Tuple arguments (2).
        interval = hzgfx.interval.interval( ( 2.0, 4.0 ) )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 2.0, interval.start )
        self.assertEqual( 4.0, interval.stop )
        self.assertEqual( 1, interval.step )

        # Tuple arguments (3).
        interval = hzgfx.interval.interval( ( 2.0, 4.0, 0.2 ) )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 2.0, interval.start )
        self.assertEqual( 4.0, interval.stop )
        self.assertEqual( 0.2, interval.step )

        # Mixed tuple arguments.
        interval = hzgfx.interval.interval( ( 2, 8.0, 2 ) )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 2.0, interval.start )
        self.assertEqual( 8.0, interval.stop )
        self.assertEqual( 2, interval.step )

        # Mixed arguments.
        interval = hzgfx.interval.interval( 2, 8.0 )
        self.assertIsInstance( interval, hzgfx.interval.RealInterval )
        self.assertEqual( 2.0, interval.start )
        self.assertEqual( 8.0, interval.stop )
        self.assertEqual( 1, interval.step )


#=============================================================================
class TestInterval( unittest.TestCase ):
    """
    Tests the Interval class.
    """


    #=========================================================================
    def test_init( self ):
        """
        Tests the __init__ method.
        """

        # Width-specified, integer interval
        interval = hzgfx.interval.Interval( 10 )
        self.assertEqual( 0, interval.start )
        self.assertEqual( 10, interval.stop )
        self.assertEqual( 1, interval.step )

        # Extreme-specified, integer interval
        interval = hzgfx.interval.Interval( 3, 8 )
        self.assertEqual( 3, interval.start )
        self.assertEqual( 8, interval.stop )
        self.assertEqual( 1, interval.step )

        # Extreme-specified, integer interval, with alternate step
        interval = hzgfx.interval.Interval( 0, 4, 2 )
        self.assertEqual( 0, interval.start )
        self.assertEqual( 4, interval.stop )
        self.assertEqual( 2, interval.step )

        # Width-specified, float interval
        interval = hzgfx.interval.Interval( 1.0 )
        self.assertEqual( 0.0, interval.start )
        self.assertEqual( 1.0, interval.stop )
        self.assertEqual( 1.0, interval.step )

        # Extreme-specified, float interval
        interval = hzgfx.interval.Interval( 3.5, 8.2 )
        self.assertAlmostEqual( 3.5, interval.start )
        self.assertAlmostEqual( 8.2, interval.stop )
        self.assertEqual( 1.0, interval.step )

        # Extreme-specified, float interval, with alternate step
        interval = hzgfx.interval.Interval( 0.0, 0.4, 0.2 )
        self.assertAlmostEqual( 0.0, interval.start )
        self.assertAlmostEqual( 0.4, interval.stop )
        self.assertAlmostEqual( 0.2, interval.step )


    #=========================================================================
    def test_getattr( self ):
        """
        Tests the __getattr__ method.
        """
        interval = hzgfx.interval.Interval( 0, 8, 2 )
        self.assertEqual( 8, interval.delta )
        interval = hzgfx.interval.Interval( -3.1, 8.3, 0.5 )
        self.assertAlmostEqual( 11.4, interval.delta )
        with self.assertRaises( AttributeError ):
            dummy = interval.fakeyfaker


    #=========================================================================
    def test_getitem( self ):
        """
        Tests the __getitem__ method.
        """
        interval = hzgfx.interval.Interval( 0, 8, 2 )
        self.assertEqual( 0, interval[ 0 ] )
        self.assertEqual( 2, interval[ 1 ] )
        self.assertEqual( 4, interval[ 2 ] )
        self.assertEqual( 6, interval[ 3 ] )
        self.assertEqual( 8, interval[ 4 ] )
        self.assertEqual( 6, interval[ -1 ] )
        self.assertEqual( 4, interval[ -2 ] )
        self.assertEqual( 2, interval[ -3 ] )
        self.assertEqual( 0, interval[ -4 ] )
        self.assertEqual( -2, interval[ -5 ] )
        interval = hzgfx.interval.Interval( 0.0, 0.4, 0.2 )
        self.assertAlmostEqual( 0.0, interval[ 0 ] )
        self.assertAlmostEqual( 0.2, interval[ 1 ] )
        self.assertAlmostEqual( 0.4, interval[ 2 ] )
        self.assertAlmostEqual( 0.6, interval[ 3 ] )
        self.assertAlmostEqual( 0.2, interval[ -1 ] )
        self.assertAlmostEqual( 0.0, interval[ -2 ] )
        self.assertAlmostEqual( -0.2, interval[ -3 ] )
        interval = hzgfx.interval.Interval( 0, 10 )
        self.assertEqual( 0, interval[ 0.0 ] )
        self.assertEqual( 1, interval[ 0.1 ] )
        self.assertEqual( 9, interval[ 0.9 ] )
        self.assertEqual( 10, interval[ 1.0 ] )


    #=========================================================================
    def test_iter( self ):
        """
        Tests the __iter__ method.
        """

        # Iterating over integers (works like `range()`)
        interval = hzgfx.interval.Interval( 10 )
        expected = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        actual = list( interval )
        self.assertListEqual( expected, actual )
        actual = []
        for value in interval:
            actual.append( value )
        self.assertListEqual( expected, actual )

        # Iterating over floats
        interval = hzgfx.interval.Interval( 1.0, 4.0, 0.5 )
        expected = [ 1.0, 1.5, 2.0, 2.5, 3.0, 3.5 ]
        actual = list( interval )
        self.assertListEqual( expected, actual )
        actual = []
        for value in interval:
            actual.append( value )
        self.assertListEqual( expected, actual )


    #=========================================================================
    def test_len( self ):
        """
        Tests the __len__ method.
        """

        # Integer intervals
        interval = hzgfx.interval.Interval( 10 )
        self.assertEqual( 10, len( interval ) )
        interval = hzgfx.interval.Interval( 0, 8 )
        self.assertEqual( 8, len( interval ) )
        interval = hzgfx.interval.Interval( 0, 8, 2 )
        self.assertEqual( 4, len( interval ) )
        interval = hzgfx.interval.Interval( 0, 7, 2 )
        self.assertEqual( 3, len( interval ) )

        # Float intervals
        interval = hzgfx.interval.Interval( 2.0 )
        self.assertEqual( 2, len( interval ) )
        interval = hzgfx.interval.Interval( 5.0, 9.0 )
        self.assertEqual( 4, len( interval ) )
        interval = hzgfx.interval.Interval( 0.2, 0.8, 0.2 )
        self.assertEqual( 3, len( interval ) )
        interval = hzgfx.interval.Interval( 0.2, 0.7, 0.2 )
        self.assertEqual( 2, len( interval ) )


    #=========================================================================
    def test_str( self ):
        """
        Tests the __str__ method.
        """
        interval = hzgfx.interval.Interval( 0, 8, 2 )
        self.assertEqual( '[0:8:2]', str( interval ) )
        interval = hzgfx.interval.Interval( -3.1, 8.3, 0.5 )
        self.assertEqual( '[-3.1:8.3:0.5]', str( interval ) )


#=============================================================================
class TestRealInterval( unittest.TestCase ):
    """
    Tests the RealInterval class.
    """


    #=========================================================================
    def test_getitem( self ):
        """
        Tests the __getitem__ method with new __len__ method.
        """
        interval = hzgfx.interval.RealInterval( 0, 4, 2 )
        self.assertEqual( 0, interval[ 0 ] )
        self.assertEqual( 2, interval[ 1 ] )
        self.assertEqual( 4, interval[ 2 ] )
        self.assertEqual( 4, interval[ -1 ] )
        self.assertEqual( 2, interval[ -2 ] )
        self.assertEqual( 0, interval[ -3 ] )
        self.assertEqual( -2, interval[ -4 ] )
        interval = hzgfx.interval.RealInterval( 0.0, 0.4, 0.2 )
        self.assertAlmostEqual( 0.0, interval[ 0 ] )
        self.assertAlmostEqual( 0.2, interval[ 1 ] )
        self.assertAlmostEqual( 0.4, interval[ 2 ] )
        self.assertAlmostEqual( 0.6, interval[ 3 ] )
        self.assertAlmostEqual( 0.4, interval[ -1 ] )
        self.assertAlmostEqual( 0.2, interval[ -2 ] )
        self.assertAlmostEqual( 0.0, interval[ -3 ] )
        self.assertAlmostEqual( -0.2, interval[ -4 ] )
        interval = hzgfx.interval.RealInterval( 0, 9 )
        self.assertEqual( 0, interval[ 0.0 ] )
        self.assertEqual( 1, interval[ 0.1 ] )
        self.assertEqual( 9, interval[ 0.9 ] )
        self.assertEqual( 10, interval[ 1.0 ] )


    #=========================================================================
    def test_iter( self ):
        """
        Tests the __iter__ method with new __len__ method.
        """

        # Iterating over integers
        interval = hzgfx.interval.RealInterval( 10 )
        expected = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
        actual = list( interval )
        self.assertListEqual( expected, actual )
        actual = []
        for value in interval:
            actual.append( value )
        self.assertListEqual( expected, actual )

        # Iterating over floats
        interval = hzgfx.interval.RealInterval( 1.0, 4.0, 0.5 )
        expected = [ 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0 ]
        actual = list( interval )
        self.assertListEqual( expected, actual )
        actual = []
        for value in interval:
            actual.append( value )
        self.assertListEqual( expected, actual )


    #=========================================================================
    def test_len( self ):
        """
        Tests the __len__ method.
        """

        # Integer intervals
        interval = hzgfx.interval.RealInterval( 10 )
        self.assertEqual( 11, len( interval ) )
        interval = hzgfx.interval.RealInterval( 0, 8 )
        self.assertEqual( 9, len( interval ) )
        interval = hzgfx.interval.RealInterval( 0, 8, 2 )
        self.assertEqual( 5, len( interval ) )
        interval = hzgfx.interval.RealInterval( 0, 7, 2 )
        self.assertEqual( 4, len( interval ) )

        # Float intervals
        interval = hzgfx.interval.RealInterval( 1.0 )
        self.assertEqual( 2, len( interval ) )
        interval = hzgfx.interval.RealInterval( 2.0 )
        self.assertEqual( 3, len( interval ) )
        interval = hzgfx.interval.RealInterval( 5.0, 9.0 )
        self.assertEqual( 5, len( interval ) )
        interval = hzgfx.interval.RealInterval( 0.2, 0.8, 0.2 )
        self.assertEqual( 4, len( interval ) )
        interval = hzgfx.interval.RealInterval( 0.2, 0.7, 0.2 )
        self.assertEqual( 3, len( interval ) )


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main()

