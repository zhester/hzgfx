#=============================================================================
#
# Cartesian Coordinate Plane Mapping
#
# A recurring need in graphical programming is mapping one Cartesian
# coordinate system onto another.  Writing the same proportional mapping code
# in every program feels wrong, and seems like a simple class could get rid of
# a lot of comments explaining the transforms each time.
#
#=============================================================================

"""
Cartesian Coordinate Plane Mapping
==================================

Each Cartesian plane is modeled independently.  Conversion between planes is
handled by several methods designed to handle outside instances which, in
turn, provides a system to "chain" any number of planes together to create
translations between multiple planes at once.

In the end, the purpose is to turn a coordinate pair in one plane into a
coordinate pair for another plane.  The mapped coordinates should be
_visually_ identical when viewed on grids of equal aspect ratios.

Mapping Methods
---------------

Coordinate mapping can be performed in a number of ways.

### Scaling

Scaling is used when the full range of coordinates must match between the
input and the output.  Thus, the ranges are scaled such that their extremes
are considered equal positions.

### Clamping

Clamping is used when only a portion of one range must match another range.
When clamping, information is usually eliminated at the extremes of a range.

### Filling

Filling can be used to preserve a target range without proportional distortion
in a source range.  When filling, a "matte" (letterbox) effect can result if
the ranges are not directly mapped.

Specifying Coordinates and Dimensions
-------------------------------------

Most coordinates and dimensions are given in pairs.  Thus, this system uses
two-tuples to communicate coordinates.  Internally, these pairs are converted
to a Point named tuple.

"""


import collections


__version__ = '0.0.0'


#=============================================================================
# Constants used for interfaces
AXIS_NONE       = 0
AXIS_HORIZONTAL = 1
AXIS_VERTICAL   = 2
AXIS_BOTH       = ( AXIS_HORIZONTAL | AXIS_VERTICAL )


#=============================================================================
# Two-tuples for specifying coordinates, dimensions, and coefficients
Point     = collections.namedtuple( 'Point',        ( 'x', 'y' ) )
Dimension = collections.namedtuple( 'Dimension',    ( 'w', 'h' ) )
SILine    = collections.namedtuple( 'SILine', ( 'm', 'b' ) )


#=============================================================================
class Axis( object ):
    """
    Models a single linear axis.
    """


    #=========================================================================
    def __init__( self, start, stop = None, step = 1 ):
        """
        Initializes an Axis object.

        @param start The left/top extreme of the coodinate plane
                     If `stop` is not given, this is used as the extent
                     (number of values) on the axis
        @param stop  The bottom/right extreme of the coodinate plane
        @param step  The difference between adjacent values in the axis.  If
                     not given, the default is 1.
        """

        # Set coordinate value type.
        self.type  = type( start )

        # Look for length-specified axis.
        if stop is None:
            self.start = self.type( 0 )
            self.stop  = start - 1

        # Use extreme-specified axis.
        else:
            self.start = start
            self.stop  = stop

        # Set the step size.
        self.step = self.type( step )


    #=========================================================================
    def __len__( self ):
        """
        Produces the length of the axis as a number of steps over the range.

        @return The numeric length of discrete values in the axis
        """
        return abs( ( self.stop - self.start ) / self.step )


    #=========================================================================
    def __str__( self ):
        """
        Produces a string representation of the axis.

        @return A string representation of the axis
        """
        return '[{0.start}:{0.stop}:{0.step}]'.format( self )


    #=========================================================================
    def extent( self ):
        """
        Produces the numeric extent of the axis from one extreme to the other.

        @return The distance from the start coordinate to the stop coordinate,
                with negative distances indicating right/bottom start coords
        """
        return self.stop - self.start


#=============================================================================
class Plane( object ):
    """
    Models a Cartesian coordinate plane.
    """


    #=========================================================================
    def __init__(
        self,
        topleft,
        bottomright = None,
        xstep       = 1,
        ystep       = None
    ):
        """
        Initializes a Plane object.

        Note: Coordinates are given as two-tuples of (x,y) coordinate pairs.
        Note: Dimensions are given as two-tuples of (w,h) size pairs.

        @param topleft     If `bottomright` is not given, this specifies the
                           width and height of the plane assuming the origin
                           (0,0) is at the top, left corner of the plane.
                           Otherwise, this specifies the coordinates of the
                           top, left extreme of the plane
        @param bottomright If specified, gives coordinates of the bottom,
                           right extreme of the plane
        @param xstep       The distance between horizontal coordinates,
                           defaults to 1
        @param ystep       The distance between vertical coordinates,
                           defaults to `xstep`
        """

        # Set up basic coordinate information.
        self._cmake = Point
        self._dmake = Dimension
        self._xtype = type( topleft[ 0 ] )
        self._ytype = type( topleft[ 1 ] )

        # Default the vertical step value.
        ystep = ystep if ystep is not None else xstep

        # Check for width/height initialization.
        if bottomright is None:

            # Create the axes.
            self._x = Axis( self._xtype( 0 ), topleft[ 0 ], xstep )
            self._y = Axis( self._ytype( 0 ), topleft[ 1 ], ystep )

        # Both extremes are given
        else:

            # Create the axes.
            self._x = Axis( topleft[ 0 ], bottomright[ 0 ], xstep )
            self._y = Axis( topleft[ 1 ], bottomright[ 1 ], ystep )


    #=========================================================================
    def __getattr__( self, name ):
        """
        Procedurally-generated attributes.

        aspect         The width/height aspect ratio (can be negative)
        bottomright|br The (x,y) coordinate of the bottom-right extreme
        dimensions|dim The (w,h) dimensions of the plane
        height|h       The number of coordinates on the vertical axis
        topleft|tl     The (x,y) coordinate of the top-left extreme
        width|w        The number of coordinates on the horizontal axis

        @param name The name of the attribute to retrieve
        @return     The value of the requested attribute
        """
        if ( name == 'dimensions' ) or ( name == 'dim' ):
            return self._dmake( len( self._x ), len( self._y ) )
        elif name == 'aspect':
            return self._x.extent() / self._y.extent()
        elif name == 'top':
            return self._y.start
        elif name == 'left':
            return self._x.start
        elif name == 'bottom':
            return self._y.stop
        elif name == 'right':
            return self._x.stop
        elif ( name == 'topleft' ) or ( name == 'tl' ):
            return self._cmake( self._x.start, self._y.start )
        elif ( name == 'bottomright' ) or ( name == 'br' ):
            return self._cmake( self._x.stop, self._y.stop )
        elif ( name == 'width') or ( name == 'w' ):
            return len( self._x )
        elif ( name == 'height' ) or ( name == 'h' ):
            return len( self._y )
        elif name == 'xextent':
            return self._x.extent()
        elif name == 'yextent':
            return self._y.extent()
        raise AttributeError( 'Unknown attribute: {}'.format( name ) )


    #=========================================================================
    def __str__( self ):
        """
        Produces a string representation of the Cartesian plane.

        @return A string representation of the Cartesian plane
        """
        return 'X := {}; Y := {}'.format( self._x, self._y )


#=============================================================================
class ComplexPlane( Plane ):
    """
    Extends the Cartesian Coordinate Plane class to support complex numbers.
    """
    pass


#=============================================================================
class Map( object ):
    """
    Models coordinate mapping between two planes.
    """


    #=========================================================================
    def __init__( self, horizontal = None, vertical = None ):
        """
        Initializes a Map object.

        Note: Linear map coefficients are given as two-tuples or SILine named
        tuples where the first item is the straight-line slope, and the second
        item is the straight-line intercept.

        @param horizontal Linear map coefficients from horizontal coordinates
                          from an source plane to a target plane.  When not
                          specified, the map defaults to a 1:1 scaled map with
                          matching origins.
        @param vertical   Same as `horizontal`, but for the vertical axis
        """
        if horizontal is None:
            self.horizontal = SILine( 1.0, 0.0 )
        else:
            self.horizontal = SILine( *horizontal )
        if vertical is None:
            self.vertical = SILine( 1.0, 0.0 )
        else:
            self.vertical = SILine( *vertical )


    #=========================================================================
    @staticmethod
    def map_extremes( source, target ):
        """
        Creates new map objects based on the extremes of two planes.

        @param source The source plane for mapping requests
        @param target The target plane for mapping requests
        @return       A new Map instance for scaled coordinate mapping
        """
        xslope     = target.xextent / source.xextent
        xintercept = target.topleft.x - xslope * source.topleft.x
        yslope     = target.yextent / source.yextent
        yintercept = target.topleft.y - yslope * source.topleft.y
        return Map( ( xslope, xintercept ), ( yslope, yintercept ) )


    #=========================================================================
    @staticmethod
    def map_clipped( source, target, fixed = HORIZONTAL ):
        """
        Creates new map objects that clip the source plane within the
        boundaries of the target plane.

        Clipping assumes one dimension is fixed, and the other is scaled
        assuming each point in the planes map with an equal aspect ratio.

        @param source The source plane for mapping requests
        @param target The target plane for mapping requests
        @return       A new Map instance for clipped coordinate mapping
        """

        # Clip the horizontal axis with respect to the vertical axis.
        if fixed == VERTICAL:
            ### ZIH
            pass

        # Clip the vertical axis with respect to the horizontal axis.
        else:

            # Determine vertical scaling for target plane.
            vertscale = abs( target.xextent ) * source.height / source.width

            # Determine the vertical middle point of the target plane.
            vertmid = target.top + abs( target.yextent ) / 2.0

            # Determine new vertical extremes for the target plane.
            ### ZIH
            #ytop = vertmid -
            #ybot = vertmid +

            # Determine slope and intercept for the vertical axis mapping.

            # Create Map object with adjusted vertical axis.

