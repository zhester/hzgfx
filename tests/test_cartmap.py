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
import hzgfx.interval



#=============================================================================
class TestLinearMap( unittest.TestCase ):
    """
    Tests the LinearMap class.
    """


    #=========================================================================
    def test_init( self ):
        """
        Tests the __init__ method.
        """

        # Make sure both intervals are validated during intialization.
        with self.assertRaises( ValueError ):
            lmap = hzgfx.cartmap.LinearMap( ( 0, 0 ), ( 0, 5 ) )
        with self.assertRaises( ValueError ):
            lmap = hzgfx.cartmap.LinearMap( ( 0, 5 ), ( 0, 0 ) )

        # Check for proper use of existing intervals.
        source = hzgfx.interval.Interval( 0, 10 )
        target = hzgfx.interval.Interval( 0, 10 )
        lmap = hzgfx.cartmap.LinearMap( source, target )
        self.assertIs( source, lmap.source )
        self.assertIs( target, lmap.target )

        # Make sure intervals can be magically constructed.
        lmap = hzgfx.cartmap.LinearMap( ( 0, 5 ), ( 0, 5 ) )
        self.assertIsInstance( lmap.source, hzgfx.interval.Interval )
        self.assertIsInstance( lmap.target, hzgfx.interval.Interval )
        lmap = hzgfx.cartmap.LinearMap( ( 0.0, 1.0 ), ( 0.0, 1.0 ) )
        self.assertIsInstance( lmap.source, hzgfx.interval.RealInterval )
        self.assertIsInstance( lmap.target, hzgfx.interval.RealInterval )

        # Check a few internal intializations.
        ### ZIH
        # lmap._map
        # lmap._clip
        # lmap._fill


    #=========================================================================
    def test_translate( self ):
        """
        Tests the translate and __getitem__ methods.
        """

        # Simple direct mapping.
        lmap = hzgfx.cartmap.LinearMap( ( 0, 4 ), ( 0, 4 ) )
        self.assertEqual( 0, lmap[ 0 ] )
        self.assertEqual( 1, lmap[ 1 ] )
        self.assertEqual( 2, lmap[ 2 ] )
        self.assertEqual( 3, lmap[ 3 ] )

        # Simple continuous mapping.
        lmap = hzgfx.cartmap.LinearMap( ( 0.0, 1.0 ), ( 0.0, 1.0 ) )
        self.assertAlmostEqual( 0.0, lmap[ 0.0 ] )
        self.assertAlmostEqual( 0.1, lmap[ 0.1 ] )
        self.assertAlmostEqual( 0.5, lmap[ 0.5 ] )
        self.assertAlmostEqual( 1.0, lmap[ 1.0 ] )

        # Simple scaled mapping.
        lmap = hzgfx.cartmap.LinearMap( ( 0.0, 1.0 ), ( 0.0, 10.0 ) )
        self.assertAlmostEqual( 0.0, lmap[ 0.0 ] )
        self.assertAlmostEqual( 1.0, lmap[ 0.1 ] )
        self.assertAlmostEqual( 5.0, lmap[ 0.5 ] )
        self.assertAlmostEqual( 10.0, lmap[ 1.0 ] )

        ### ZIH
        # Zero-crossing mapping.
        # Skewed mapping.
        # Inverted mapping.


#=============================================================================
class TestPlane( unittest.TestCase ):
    """
    Tests the Plane class.
    """


    #=========================================================================
    def test_init( self ):
        """
        Tests the __init__ method.
        """
        plane = hzgfx.cartmap.Plane( 25 )
        plane = hzgfx.cartmap.Plane( 2.0 )
        plane = hzgfx.cartmap.Plane( ( 2, 2.0 ) )
        ### ZIH


    #=========================================================================
    def test_init_int( self ):
        """
        Tests the __init__ method for integer planes.
        """
        plane = hzgfx.cartmap.Plane( 25 )
        self.assertEqual( 25, len( plane._x ) )
        self.assertEqual( 25, len( plane._y ) )
        self.assertEqual( 25, plane._x.delta )
        self.assertEqual( 25, plane._y.delta )
        plane = hzgfx.cartmap.Plane( ( 100, 50 ) )
        self.assertEqual( 100, len( plane._x ) )
        self.assertEqual( 50, len( plane._y ) )
        self.assertEqual( 100, plane._x.delta )
        self.assertEqual( 50, plane._y.delta )
        plane = hzgfx.cartmap.Plane( ( -10, -5 ), ( 10, 5 ) )
        self.assertEqual( 20, len( plane._x ) )
        self.assertEqual( 10, len( plane._y ) )
        self.assertEqual( 20, plane._x.delta )
        self.assertEqual( 10, plane._y.delta )
        plane = hzgfx.cartmap.Plane( ( -10, -5 ), ( 10, 5 ), 2 )
        self.assertEqual( 10, len( plane._x ) )
        self.assertEqual( 5, len( plane._y ) )
        self.assertEqual( 20, plane._x.delta )
        self.assertEqual( 10, plane._y.delta )
        plane = hzgfx.cartmap.Plane( ( -10, -5 ), ( 10, 5 ), ( 2, 1 ) )
        self.assertEqual( 10, len( plane._x ) )
        self.assertEqual( 10, len( plane._y ) )
        self.assertEqual( 20, plane._x.delta )
        self.assertEqual( 10, plane._y.delta )


    #=========================================================================
    def test_init_float( self ):
        """
        Tests the __init__ method for float planes.
        """
        plane = hzgfx.cartmap.Plane( 2.0 )
        self.assertEqual( 2.0, len( plane._x ) )
        self.assertEqual( 2.0, len( plane._y ) )
        self.assertEqual( 2.0, plane._x.delta )
        self.assertEqual( 2.0, plane._y.delta )
        plane = hzgfx.cartmap.Plane( ( 5.0, 3.0 ) )
        self.assertEqual( 5.0, len( plane._x ) )
        self.assertEqual( 3.0, len( plane._y ) )
        self.assertEqual( 5.0, plane._x.delta )
        self.assertEqual( 3.0, plane._y.delta )
        plane = hzgfx.cartmap.Plane( ( -10.0, -5.0 ), ( 10.0, 5.0 ) )
        self.assertEqual( 20.0, len( plane._x ) )
        self.assertEqual( 10.0, len( plane._y ) )
        self.assertEqual( 20.0, plane._x.delta )
        self.assertEqual( 10.0, plane._y.delta )
        plane = hzgfx.cartmap.Plane( ( -10.0, -5.0 ), ( 10.0, 5.0 ), 2.0 )
        self.assertEqual( 10.0, len( plane._x ) )
        self.assertEqual( 5.0, len( plane._y ) )
        self.assertEqual( 20.0, plane._x.delta )
        self.assertEqual( 10.0, plane._y.delta )
        plane = hzgfx.cartmap.Plane(
            ( -10.0, -5.0 ),
            ( 10.0, 5.0 ),
            ( 2.0, 1.0 )
        )
        self.assertEqual( 10.0, len( plane._x ) )
        self.assertEqual( 10.0, len( plane._y ) )
        self.assertEqual( 20.0, plane._x.delta )
        self.assertEqual( 10.0, plane._y.delta )


    #=========================================================================
    def test_getitem( self ):
        """
        Tests the __getitem__ method.
        """
        plane = hzgfx.cartmap.Plane(
            ( 1.0, 3.0 ),
            ( 3.0, 4.0 ),
            ( 0.2, 0.1 )
        )
        self.assertAlmostEqual( 2.0, plane.aspect )
        self.assertAlmostEqual( 4.0, plane.bottom )
        self.assertAlmostEqual( 4.0, plane.b )
        exp_d = hzgfx.cartmap.Dimension( 2.0, 1.0 )
        self.assertTupleEqual( exp_d, plane.delta )
        self.assertTupleEqual( exp_d, plane.d )
        self.assertEqual( 2.0, plane.deltax )
        self.assertEqual( 2.0, plane.dx )
        self.assertEqual( 1.0, plane.deltay )
        self.assertEqual( 1.0, plane.dy )
        exp_dim = hzgfx.cartmap.Dimension( 10, 10 )
        self.assertTupleEqual( exp_dim, plane.dimensions )
        self.assertTupleEqual( exp_dim, plane.dim )
        self.assertEqual( 10, plane.height )
        self.assertEqual( 10, plane.h )
        self.assertAlmostEqual( 1.0, plane.left )
        self.assertAlmostEqual( 1.0, plane.l )
        exp_lt = hzgfx.cartmap.Point( 1.0, 3.0 )
        self.assertTupleEqual( exp_lt, plane.lefttop )
        self.assertTupleEqual( exp_lt, plane.lt )
        self.assertAlmostEqual( 3.0, plane.right )
        self.assertAlmostEqual( 3.0, plane.r )
        exp_rb = hzgfx.cartmap.Point( 3.0, 4.0 )
        self.assertTupleEqual( exp_rb, plane.rightbot )
        self.assertTupleEqual( exp_rb, plane.rb )
        self.assertAlmostEqual( 3.0, plane.top )
        self.assertAlmostEqual( 3.0, plane.t )
        self.assertEqual( 10, plane.width )
        self.assertEqual( 10, plane.w )
        with self.assertRaises( AttributeError ):
            dummy = plane.fakeyfaker


    #=========================================================================
    def test_str( self ):
        """
        Tests the __str__ method.
        """
        plane = hzgfx.cartmap.Plane(
            ( 10, 20 ),
            ( 30, 40 ),
            ( 2, 4 )
        )
        expected = 'X := [10,30);2 / Y := [20,40);4'
        self.assertEqual( expected, str( plane ) )


#=============================================================================
class TestMap( unittest.TestCase ):
    """
    Tests the Map class.
    """


    #=========================================================================
    def test_init( self ):
        """
        Tests the __init__ method.
        """
        pmap = hzgfx.cartmap.Map()
        exp_siline = hzgfx.cartmap.Line( 1.0, 0.0 )
        self.assertTupleEqual( exp_siline, pmap.horizontal )
        self.assertTupleEqual( exp_siline, pmap.vertical )
        pmap = hzgfx.cartmap.Map( ( 1.0, 10.0 ), ( -1.0, 0.0 ) )
        exp_hline = hzgfx.cartmap.Line( 1.0, 10.0 )
        exp_vline = hzgfx.cartmap.Line( -1.0, 0.0 )
        self.assertTupleEqual( exp_hline, pmap.horizontal )
        self.assertTupleEqual( exp_vline, pmap.vertical )


    #=========================================================================
    def test_map_extremes( self ):
        """
        Tests the map_extremes method.
        """
        splane = hzgfx.cartmap.Plane( 100 )
        tplane = hzgfx.cartmap.Plane( 25 )
        pmap = hzgfx.cartmap.Map.map_extremes( splane, tplane )
        exp_hline = hzgfx.cartmap.Line( 0.25, 0.0 )
        exp_vline = hzgfx.cartmap.Line( 0.25, 0.0 )
        self.assertTupleEqual( exp_hline, pmap.horizontal )
        self.assertTupleEqual( exp_vline, pmap.vertical )


    #=========================================================================
    def test_map_clipped( self ):
        """
        Tests the map_clipped method.
        """
        splane = hzgfx.cartmap.Plane( ( 100, 50 ) )
        tplane = hzgfx.cartmap.Plane( (  25, 25 ) )
        pmap = hzgfx.cartmap.Map.map_clipped( splane, tplane )
        exp_hline = hzgfx.cartmap.Line( 0.25, 0.0 )
        exp_vline = hzgfx.cartmap.Line( 0.25, 6.25 )
        self.assertTupleEqual( exp_hline, pmap.horizontal )
        self.assertTupleEqual( exp_vline, pmap.vertical )


    #=========================================================================
    def test_translate( self ):
        """
        Tests the translate method.
        """

        # Test a mapping between a source and a vertically-clipped target.
        splane = hzgfx.cartmap.Plane( ( 100, 50 ) )
        tplane = hzgfx.cartmap.Plane( (  25, 25 ) )
        pmap = hzgfx.cartmap.Map.map_clipped( splane, tplane )
        exp_origin = hzgfx.cartmap.Point( 0.0, 6.25 )
        self.assertTupleEqual( exp_origin, pmap.translate() )
        exp_point = hzgfx.cartmap.Point( 2.5, 12.5 )
        self.assertTupleEqual( exp_point, pmap.translate( ( 10, 25 ) ) )
        exp_point = hzgfx.cartmap.Point( 3, 13 )
        point = pmap.translate( ( 10, 25 ), True )
        self.assertTupleEqual( exp_point, point )
        exp_point = hzgfx.cartmap.Point( 2.5, 13 )
        point = pmap.translate( ( 10, 25 ), ( False, True ) )
        self.assertTupleEqual( exp_point, point )

        ### ZIH - test horizontally-clipped targets
        ### ZIH - test scaled mapping with map_extremes
        ### ZIH - test negative extremes, centered origins, off-centered


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main()

