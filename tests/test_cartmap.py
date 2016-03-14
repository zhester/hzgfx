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
    def setUp( self ):
        """
        Performs common test setup.
        """
        self.i010  = hzgfx.interval.Interval( 0, 10 )
        self.i100  = hzgfx.interval.Interval( 10, 0 )
        self.r01   = hzgfx.interval.RealInterval( 0.0, 1.0, 0.1 )
        self.r10   = hzgfx.interval.RealInterval( 1.0, 0.0, 0.1 )
        self.lm_i1 = hzgfx.cartmap.LinearMap( self.i010, self.i010 )
        self.lm_i2 = hzgfx.cartmap.LinearMap( self.i010, self.i100 )
        self.lm_r1 = hzgfx.cartmap.LinearMap( self.r01, self.r01 )
        self.lm_r2 = hzgfx.cartmap.LinearMap( self.r01, self.r10 )


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
        self.assertIsInstance( self.lm_i1._map, hzgfx.cartmap.Line )
        self.assertEqual( 1.0, self.lm_i1._map.a )
        self.assertEqual( 0.0, self.lm_i1._map.b )
        self.assertIsNone( self.lm_i1._clip )
        self.assertIsNone( self.lm_i1._fill )


    #=========================================================================
    def test_clipped( self ):
        """
        Tests clipped mapping.
        """

        # Simple direct mapping.
        lmap = hzgfx.cartmap.LinearMap( ( 0, 8 ), ( 0, 8 ) )

        # Ensure no clipping is enabled.
        self.assertIsNone( lmap._clip )
        self.assertEqual( 0, lmap[ 0 ] )
        self.assertEqual( 7, lmap[ 7 ] )

        # Enable clipping from target interval.
        # This clips half the domain (1/4 on each end).
        # This results in an effective output step of 0.5.
        lmap.set_clip( ( 2, 6 ) )

        # Internal state test.
        self.assertIsNotNone( lmap._clip )
        self.assertIsInstance( lmap._clip, hzgfx.interval.Interval )

        # Clipping test.
        self.assertEqual( 2.0, lmap[ 0 ] )
        self.assertEqual( 2.5, lmap[ 1 ] )
        self.assertEqual( 3.0, lmap[ 2 ] )
        self.assertEqual( 3.5, lmap[ 3 ] )
        self.assertEqual( 4.0, lmap[ 4 ] )
        self.assertEqual( 4.5, lmap[ 5 ] )
        self.assertEqual( 5.0, lmap[ 6 ] )
        self.assertEqual( 5.5, lmap[ 7 ] )


    #=========================================================================
    def test_filled( self ):
        """
        Tests filled mapping.
        """

        # Simple direct mapping.
        lmap = hzgfx.cartmap.LinearMap( ( 0, 8 ), ( 0, 8 ) )

        # Ensure no filling is enabled.
        self.assertIsNone( lmap._fill )
        self.assertEqual( 0, lmap[ 0 ] )
        self.assertEqual( 7, lmap[ 7 ] )

        # Enable filling from target interval.
        # This fills half the domain (1/4 on each end).
        # This results in an effective output step of 2.
        lmap.set_fill( ( 2, 6 ) )

        # Internal state test.
        self.assertIsNotNone( lmap._fill )
        self.assertIsInstance( lmap._fill, hzgfx.interval.Interval )

        # Filling test.
        self.assertEqual( -4.0, lmap[ 0 ] )
        self.assertEqual( -2.0, lmap[ 1 ] )
        self.assertEqual(  0.0, lmap[ 2 ] )
        self.assertEqual(  2.0, lmap[ 3 ] )
        self.assertEqual(  4.0, lmap[ 4 ] )
        self.assertEqual(  6.0, lmap[ 5 ] )
        self.assertEqual(  8.0, lmap[ 6 ] )
        self.assertEqual( 10.0, lmap[ 7 ] )


    #=========================================================================
    def test_clipped_filled( self ):
        """
        Tests clipped and filled mapping.
        """

        # Simple direct mapping.
        lmap = hzgfx.cartmap.LinearMap( ( 0, 8 ), ( 0, 8 ) )

        # Ensure no clipping or filling is enabled.
        self.assertIsNone( lmap._clip )
        self.assertIsNone( lmap._fill )
        self.assertEqual( 0, lmap[ 0 ] )
        self.assertEqual( 7, lmap[ 7 ] )

        # Enable clipping and filling from target interval.
        # This particular case symmetrically clips and fills which effecitvely
        # restores the original mapping.
        lmap.set_clip( ( 2, 6 ) )
        lmap.set_fill( ( 2, 6 ) )

        # Internal state test.
        self.assertIsNotNone( lmap._clip )
        self.assertIsInstance( lmap._clip, hzgfx.interval.Interval )
        self.assertIsNotNone( lmap._fill )
        self.assertIsInstance( lmap._fill, hzgfx.interval.Interval )

        # Filling test.
        self.assertEqual( 0.0, lmap[ 0 ] )
        self.assertEqual( 1.0, lmap[ 1 ] )
        self.assertEqual( 2.0, lmap[ 2 ] )
        self.assertEqual( 3.0, lmap[ 3 ] )
        self.assertEqual( 4.0, lmap[ 4 ] )
        self.assertEqual( 5.0, lmap[ 5 ] )
        self.assertEqual( 6.0, lmap[ 6 ] )
        self.assertEqual( 7.0, lmap[ 7 ] )


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

        # Inverted mapping.
        lmap = hzgfx.cartmap.LinearMap( ( 0.0, 1.0 ), ( 1.0, 0.0 ) )
        self.assertAlmostEqual( 1.0, lmap[ 0.0 ] )
        self.assertAlmostEqual( 0.9, lmap[ 0.1 ] )
        self.assertAlmostEqual( 0.1, lmap[ 0.9 ] )
        self.assertAlmostEqual( 0.0, lmap[ 1.0 ] )

        # Mapping through origin.
        lmap = hzgfx.cartmap.LinearMap( ( 5.0, -5.0 ), ( 0, 100 ) )
        self.assertEqual( 0, lmap[ 5.0 ] )
        self.assertEqual( 25, lmap[ 2.5 ] )
        self.assertEqual( 50, lmap[ 0.0 ] )
        self.assertEqual( 75, lmap[ -2.5 ] )
        self.assertEqual( 100, lmap[ -5.0 ] )


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

