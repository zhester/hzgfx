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
        self.assertIsInstance( plane._x, hzgfx.cartmap.Axis )
        self.assertIsInstance( plane._y, hzgfx.cartmap.Axis )
        self.assertIs( plane._x.type, int )
        self.assertIs( plane._y.type, int )
        plane = hzgfx.cartmap.Plane( 2.0 )
        self.assertIs( plane._x.type, float )
        self.assertIs( plane._y.type, float )
        plane = hzgfx.cartmap.Plane( ( 2, 2.0 ) )
        self.assertIs( plane._x.type, int )
        self.assertIs( plane._y.type, float )


    #=========================================================================
    def test_init_int( self ):
        """
        Tests the __init__ method for integer planes.
        """
        plane = hzgfx.cartmap.Plane( 25 )
        self.assertEqual( 25, len( plane._x ) )
        self.assertEqual( 25, len( plane._y ) )
        self.assertEqual( 25, plane._x.delta() )
        self.assertEqual( 25, plane._y.delta() )
        plane = hzgfx.cartmap.Plane( ( 100, 50 ) )
        self.assertEqual( 100, len( plane._x ) )
        self.assertEqual( 50, len( plane._y ) )
        self.assertEqual( 100, plane._x.delta() )
        self.assertEqual( 50, plane._y.delta() )
        plane = hzgfx.cartmap.Plane( ( -10, -5 ), ( 10, 5 ) )
        self.assertEqual( 20, len( plane._x ) )
        self.assertEqual( 10, len( plane._y ) )
        self.assertEqual( 20, plane._x.delta() )
        self.assertEqual( 10, plane._y.delta() )
        plane = hzgfx.cartmap.Plane( ( -10, -5 ), ( 10, 5 ), 2 )
        self.assertEqual( 10, len( plane._x ) )
        self.assertEqual( 5, len( plane._y ) )
        self.assertEqual( 20, plane._x.delta() )
        self.assertEqual( 10, plane._y.delta() )
        plane = hzgfx.cartmap.Plane( ( -10, -5 ), ( 10, 5 ), ( 2, 1 ) )
        self.assertEqual( 10, len( plane._x ) )
        self.assertEqual( 10, len( plane._y ) )
        self.assertEqual( 20, plane._x.delta() )
        self.assertEqual( 10, plane._y.delta() )


    #=========================================================================
    def test_init_float( self ):
        """
        Tests the __init__ method for float planes.
        """
        plane = hzgfx.cartmap.Plane( 2.0 )
        self.assertEqual( 2.0, len( plane._x ) )
        self.assertEqual( 2.0, len( plane._y ) )
        self.assertEqual( 2.0, plane._x.delta() )
        self.assertEqual( 2.0, plane._y.delta() )
        plane = hzgfx.cartmap.Plane( ( 5.0, 3.0 ) )
        self.assertEqual( 5.0, len( plane._x ) )
        self.assertEqual( 3.0, len( plane._y ) )
        self.assertEqual( 5.0, plane._x.delta() )
        self.assertEqual( 3.0, plane._y.delta() )
        plane = hzgfx.cartmap.Plane( ( -10.0, -5.0 ), ( 10.0, 5.0 ) )
        self.assertEqual( 20.0, len( plane._x ) )
        self.assertEqual( 10.0, len( plane._y ) )
        self.assertEqual( 20.0, plane._x.delta() )
        self.assertEqual( 10.0, plane._y.delta() )
        plane = hzgfx.cartmap.Plane( ( -10.0, -5.0 ), ( 10.0, 5.0 ), 2.0 )
        self.assertEqual( 10.0, len( plane._x ) )
        self.assertEqual( 5.0, len( plane._y ) )
        self.assertEqual( 20.0, plane._x.delta() )
        self.assertEqual( 10.0, plane._y.delta() )
        plane = hzgfx.cartmap.Plane(
            ( -10.0, -5.0 ),
            ( 10.0, 5.0 ),
            ( 2.0, 1.0 )
        )
        self.assertEqual( 10.0, len( plane._x ) )
        self.assertEqual( 10.0, len( plane._y ) )
        self.assertEqual( 20.0, plane._x.delta() )
        self.assertEqual( 10.0, plane._y.delta() )


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
        expected = 'X := [10:30:2]; Y := [20:40:4]'
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
        exp_siline = hzgfx.cartmap.SILine( 1.0, 0.0 )
        self.assertTupleEqual( exp_siline, pmap.horizontal )
        self.assertTupleEqual( exp_siline, pmap.vertical )
        pmap = hzgfx.cartmap.Map( ( 1.0, 10.0 ), ( -1.0, 0.0 ) )
        exp_hline = hzgfx.cartmap.SILine( 1.0, 10.0 )
        exp_vline = hzgfx.cartmap.SILine( -1.0, 0.0 )
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
        exp_hline = hzgfx.cartmap.SILine( 0.25, 0.0 )
        exp_vline = hzgfx.cartmap.SILine( 0.25, 0.0 )
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
        exp_hline = hzgfx.cartmap.SILine( 0.25, 0.0 )
        exp_vline = hzgfx.cartmap.SILine( 0.25, 6.25 )
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

        ### ZIH - test horizontally-clipped targets
        ### ZIH - test scaled mapping with map_extremes
        ### ZIH - test negative extremes, centered origins, off-centered


# Run tests when run directly from the shell.
if __name__ == '__main__':
    unittest.main()

