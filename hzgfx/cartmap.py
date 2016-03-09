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

### Clipping

Clipping is used when only a portion of one range must match another range.
When clipping, information is usually eliminated at the extremes of a range.

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
Point     = collections.namedtuple( 'Point',     ( 'x', 'y' ) )
Dimension = collections.namedtuple( 'Dimension', ( 'w', 'h' ) )
SILine    = collections.namedtuple( 'SILine',    ( 'm', 'b' ) )


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
        self.type = type( start )

        # Look for length-specified axis.
        if stop is None:
            if self.type is float:
                self.start = 0.0
                self.stop  = start
            else:
                self.start = 0
                self.stop  = start

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
        delta = self.delta()
        if self.type is int:
            return abs( delta // self.step )
        return abs( delta / self.step )


    #=========================================================================
    def __str__( self ):
        """
        Produces a string representation of the axis.

        @return A string representation of the axis
        """
        if self.type is float:
            fmt = '[{0.start:.3}:{0.stop:.3}:{0.step:.3}]'
        else:
            fmt = '[{0.start}:{0.stop}:{0.step}]'
        return fmt.format( self )


    #=========================================================================
    def delta( self ):
        """
        Returns the total difference between the extreme values of the axis.

        @return The distance from the start coordinate to the stop coordinate,
                with negative distances indicating right/bottom start coords
        """
        return self.stop - self.start


#=============================================================================
class LinearMap( object ):
    """
    Models a linear mapping between two axes.
    """


    #=========================================================================
    def __init__( self, a, b ):
        """
        Initializes an LinearMap object.

        ### ZIH - also accept an output type to allow mapping to automatically
                  convert output to integers (when possibly indexing arrays on
                  axes after point translation)

        @param a The first-order linear coefficent (slope)
        @param b The constant linear coefficient (y-intercept)
        """
        self.a = a
        self.b = b


    #=========================================================================
    @staticmethod
    def map_clipped( source, target, target_limit ):
        """
        Factory method to create a new LinearMap between two Axis objects.
        Only a subsection of the target axis is mapped to the entirety of the
        source axis.
        This will result in a "clipping" effect when mapping axes of different
        lengths.

        @param source       The intended source Axis of the mapping
        @param target       The intended target Axis of the mapping
        @param target_limit ### ZIH
        @return             A LinearMap object capable of translating source
                            points to target points
        """
        ### ZIH
        pass


    #=========================================================================
    @staticmethod
    def map_scaled( source, target ):
        """
        Factory method to create a new LinearMap between two Axis objects.
        All points between axes are mapped such that the limits of each match.
        This will result in a "scaling" effect when mapping axes of different
        lengths.

        @param source The intended source Axis of the mapping
        @param target The intended target Axis of the mapping
        @return       A LinearMap object capable of translating source points
                      to target points
        """
        a = target.delta() / float( source.delta() )
        b = target.start - a * source.start
        return LinearMap( a, b )


    #=========================================================================
    def translate( self, p ):
        """
        Translates a point from an independent point on a source axis to a
        dependent point on a target axis.

        @param p The independent (input) coordinate
        @return  The dependent (output) coordinate
        """
        return self.a * p + self.b


#=============================================================================
class Plane( object ):
    """
    Models a Cartesian coordinate plane.
    """


    #=========================================================================
    def __init__(
        self,
        lefttop,
        rightbot = None,
        step     = 1
    ):
        """
        Initializes a Plane object.

        @param lefttop
            Normally, this is a two-tuple of the coordinates of the top, left
            corner of the plane.
            If the `rightbot` argument is None or not given, this specifies
            either the width and height of the plane (from a two-tuple), or
            the dimension of a squre plane (from a number).
        @param rightbot
            Normally, this is a two-tuple of the coordinate of the bottom,
            right corner of the plane.
        @param step
            The distance between individual positions in the plane.
            If given as a single number, the step is used for both axes.
            If given as a two-tuple, each axis uses its own step.
            The default step is 1.
        """

        # Coordinate and dimension constructors
        self._cmake = Point
        self._dmake = Dimension

        # Determine the step values.
        if isinstance( step, ( tuple, list ) ):
            xstep, ystep = step[ 0 : 2 ]
        else:
            xstep = step
            ystep = step

        # Check for width/height initialization.
        if rightbot is None:

            # Check for non-square plane initialization.
            if isinstance( lefttop, ( tuple, list ) ):
                left, top = lefttop[ 0 : 2 ]

            # Square plane initialization.
            else:
                top, left = lefttop, lefttop

            # Generate the default axis extremes.
            right, bot = left, top
            left, top  = type( left )( 0 ), type( top )( 0 )

        # Both extremes are given.
        else:

            # Set the axis extremes.
            left, top  = lefttop[ 0 : 2 ]
            right, bot = rightbot[ 0 : 2 ]

        # Create the axes.
        self._x = Axis( left, right, xstep )
        self._y = Axis( top, bot, ystep )


    #=========================================================================
    def __getattr__( self, name ):
        """
        Procedurally-generated attributes.

        aspect         The dx/dy aspect ratio (can be negative)
        bottom|b       The bottom vertical extreme
        delta|d        The (dx,dy) difference between extremes
        deltax|dx      The difference between horizontal extremes
        deltay|dy      The difference between veritcal extremes
        dimensions|dim The (w,h) dimensions of the plane
        height|h       The number of coordinates on the vertical axis
        left|l         The left horizontal extreme
        lefttop|lt     The (x,y) coordinate of the top-left extreme
        right|r        The right horizontal extreme
        rightbot|rb    The (x,y) coordinate of the bottom-right extreme
        top|t          The top veritical extreme
        width|w        The number of coordinates on the horizontal axis

        @param name The name of the attribute to retrieve
        @return     The value of the requested attribute
        @throws     AttributeError if the attribute is invalid
        """
        if name == 'aspect':
            return self._x.delta() / self._y.delta()
        elif ( name == 'bottom' ) or ( name == 'b' ):
            return self._y.stop
        elif ( name == 'delta' ) or ( name == 'd' ):
            return self._dmake( self._x.delta(), self._y.delta() )
        elif ( name == 'deltax' ) or ( name == 'dx' ):
            return self._x.delta()
        elif ( name == 'deltay' ) or ( name == 'dy' ):
            return self._y.delta()
        elif ( name == 'dimensions' ) or ( name == 'dim' ):
            return self._dmake( len( self._x ), len( self._y ) )
        elif ( name == 'height' ) or ( name == 'h' ):
            return len( self._y )
        elif ( name == 'left' ) or ( name == 'l' ):
            return self._x.start
        elif ( name == 'lefttop' ) or ( name == 'lt' ):
            return self._cmake( self._x.start, self._y.start )
        elif ( name == 'right' ) or ( name == 'r' ):
            return self._x.stop
        elif ( name == 'rightbot' ) or ( name == 'rb' ):
            return self._cmake( self._x.stop, self._y.stop )
        elif ( name == 'top' ) or ( name == 't' ):
            return self._y.start
        elif ( name == 'width') or ( name == 'w' ):
            return len( self._x )
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
    ### ZIH
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
        xslope     = target.deltax / float( source.deltax )
        xintercept = target.left - xslope * source.left
        yslope     = target.deltay / float( source.deltay )
        yintercept = target.left - yslope * source.left
        return Map( ( xslope, xintercept ), ( yslope, yintercept ) )


    #=========================================================================
    @staticmethod
    def map_clipped( source, target, fixed = AXIS_HORIZONTAL ):
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
        if fixed == AXIS_VERTICAL:
            ### ZIH
            pass

        # Clip the vertical axis with respect to the horizontal axis.
        else:

            # Determine new total height of the target plane.
            theight = source.deltay \
                    * float( target.deltax ) / float( source.deltax )

            # Determine the vertical middle point of the target plane.
            mid = target.top + target.deltay / 2.0

            # Determine new top vertical extreme for the target plane.
            ytop = mid - theight / 2.0

            # Determine slope and intercept for the vertical axis mapping.
            yslope     = theight / float( source.deltay )
            yintercept = ytop - yslope * source.top

            # Determine the mapping for the fixed axis.
            xslope     = target.deltax / float( source.deltax )
            xintercept = target.left - xslope * source.left

            # Create Map object with adjusted vertical axis.
            return Map( ( xslope, xintercept ), ( yslope, yintercept ) )


    #=========================================================================
    def translate( self, point = None, nearest = False ):
        """
        Translates a source point into a target point.

        @param point   A Point or two-tuple of the point to translate
        @param nearest Set to true to map outputs to the closest integer.
                       Set a two-tuple of (bool,bool) to indicate integer
                       outputs per axis.
        @return        A Point in the target plane that corresponds to the
                       same position in the source plane
        """
        if point is None:
            point = Point( 0.0, 0.0 )
        elif isinstance( point, Point ) == False:
            point = Point( *point )
        if isinstance( nearest, ( tuple, list ) ):
            nearx, neary = nearest[ 0 : 2 ]
        else:
            nearx, neary = nearest, nearest
        target_x = self.horizontal.m * point.x + self.horizontal.b
        target_y = self.vertical.m   * point.y + self.vertical.b
        if nearx:
            target_x = int( round( target_x ) )
        if neary:
            target_y = int( round( target_y ) )
        return Point( target_x, target_y )


