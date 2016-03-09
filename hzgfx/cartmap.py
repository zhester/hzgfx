#=============================================================================
#
# Cartesian Coordinate Mapping
#
# A recurring need in graphical programming is mapping one Cartesian
# coordinate system onto another.  Writing the same proportional mapping code
# in every program feels wrong, and seems like a class could get rid of a lot
# of comments explaining the transforms each time.
#
# The objective is to provide a well-defined and well-tested interface for
# converting points from one coordinate system to another.
#
# Mapping Methods
# ---------------
#
# Coordinate mapping can be performed in a number of ways.
#
# ### Scaling
#
# Scaling is used when the full range of coordinates must match between the
# input and the output.  Thus, the ranges are scaled such that their extremes
# are considered equal positions in the output.
#
# ### Clipping
#
# Clipping means that all values of a source continuum are mapped to a subset
# of the values of a target continuum.  Thus, there are values in the target
# continuum that can not be reached through the map, and are considered
# "clipped" from the output.
#
# ### Filling
#
# Filling provides the opposite functionality of clipping.  When filling, a
# subset of values of a source continuum are used to reach all values of a
# target continuum.  In this case, there are inputs that map to nothing, and
# are considered "filled" when used for output.  In an image, this typically
# results in a "letterbox" effect.
#
#=============================================================================

"""
Cartesian Coordinate Mapping
============================

### ZIH - Add user documentation.

"""


import collections
import math


__version__ = '0.0.0'


#=============================================================================
# Constants used for interfaces
AXIS_NONE       = 0
AXIS_HORIZONTAL = 1
AXIS_VERTICAL   = 2
AXIS_BOTH       = ( AXIS_HORIZONTAL | AXIS_VERTICAL )


#=============================================================================
# Two-tuples for specifying coordinates, dimensions, and coefficients
Dimension = collections.namedtuple( 'Dimension', ( 'w', 'h' ) )
Point     = collections.namedtuple( 'Point',     ( 'x', 'y' ) )
Line      = collections.namedtuple( 'Line',      ( 'a', 'b' ) )


#=============================================================================
class Interval( object ):
    """
    Models a numeric interval within a coordinate axis.

    This is modeled similarly to one of Python's numeric ranges.  The
    lower-limit of the interval is denoted as the "start" of the interval, and
    the upper-limit of the interval is denoted as the "stop" of the interval.

    The interval is specified the same way as a Python range where the
    included endpoints on the interval are [start,stop).
    """


    #=========================================================================
    def __init__( self, start, stop = None, step = 1 ):
        """
        Initializes an Interval object.

        @param start The lower-limit of the interval
                     If `stop` is not given, this is used as the `stop` value
                     of the interval, and assumes the `start` is 0.
        @param stop  One more than the upper-limit of the interval
        @param step  The distance between adjacent points in the interval
                     If not given, the default is 1.
        """

        # Look for size-specified intervals.
        if stop is None:
            self.start = type( start )( 0 )
            self.stop  = start

        # The interval is given as limits.
        else:
            self.start = start
            self.stop  = stop

        # Set the step size.
        self.step = step


    #=========================================================================
    def __getattr__( self, name ):
        """
        Provides access to computed attributes.

        Compute Attributes

        delta The difference between the upper and lower limits

        @param name The name of the attribute to retrieve
        @return     The value of the requested attribute
        @throws     AttributeError for invalid attributes
        """

        # Known attributes
        if name == 'delta':
            return self.stop - self.start

        # Unknown attribute
        raise AttributeError(
            "{} object has no attribute '{}'".format(
                self.__class__.__name__,
                name
            )
        )


    #=========================================================================
    def __getitem__( self, offset ):
        """
        Maps integer offsets into the interval to interval values.

        The difference between this and normal sequences or ranges is that
        it does not consider any offsets as invalid.  Extrapolation and
        interpolation works.

        @param offset The integer offset into the interval
                      The integer-specified slice within the interval
                      The float-specified ratio into the interval
        @return       The interval value at the offset
        @throws       KeyError if the offset can not be mapped
        """

        # Number of positions in interval.
        length = len( self )

        # Slice notation.
        if isinstance( offset, slice ):
            ### ZIH
            raise NotImplementedError()

        # Ratio of interval.
        elif type( offset ) is float:

            # Translate normal value [0.0,1.0) to offset.
            offset = int( offset * length )

        # Negative offset support.
        if offset < 0:

            # Normalize negative offset.
            offset += length

        # Interval value at this offset
        return self.start + self.step * offset


    #=========================================================================
    def __iter__( self ):
        """
        Provides an iterator interface to the interval.

        @return An iterable object for all positions on the interval
        """

        # Iterate through the normal range of the interval.
        for offset in range( len( self ) ):

            # Yield the value at each position.
            yield self.start + self.step * offset


    #=========================================================================
    def __len__( self ):
        """
        Produces the length of the interval as the number of steps between the
        lower and upper limits.

        @return The number of discrete positions in the interval
        """

        # Floor and int to avoid over-stepping the last position.
        return int( abs( self.delta / self.step ) )


    #=========================================================================
    def __str__( self ):
        """
        Produces a string representation of the interval.

        @return A string representation of the interval
        """
        return '[{0.start}:{0.stop}:{0.step}]'.format( self )


#=============================================================================
class RealInterval( Interval ):
    """
    Extends the Interval class to cleanly handle intervals of real numbers.

    Real intervals break from the convention of the "stop" value indicating
    one more than the end of the interval.  Instead, "stop" is included in the
    interval as the true upper limit.
    """


    #=========================================================================
    def __len__( self ):
        """
        Produces the length of the interval as the number of steps between the
        lower and upper limits.
        """

        # Include the limits of the interval.
        return int( abs( ( self.delta + self.step ) / self.step ) )


#=============================================================================
class LinearMap( object ):
    """
    Models a linear mapping between two intervals.
    """


    #=========================================================================
    def __init__( self, source, target, fill = None, clip = None ):
        """
        Initializes a LinearMap object.

        @param source The source Interval of the mapping
        @param target The target Interval of the mapping
        @param fill   Specify filling limits in the source
        @param clip   Specify clipping limits in the target
        """
        self.source = source
        self.target = target
        a = target.delta / float( source.delta )
        b = target.start - a * source.start
        self._scale = Line( a, b )
        ### ZIH - implement fill and clip


    #=========================================================================
    def __getitem__( self, point ):
        """
        Supports point translation through subscript notation.

        @param point A point in the source interval
        @return      The corresponding point in the target interval
        """
        return self.translate( point )


    #=========================================================================
    def translate( self, point ):
        """
        Translates a point from an independent point on a source axis to a
        dependent point on a target axis.

        @param point A point in the source interval
        @return      The corresponding point in the target interval
        """
        return self._scale.a * point + self._scale.b


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
        self._x = Interval( left, right, xstep )
        self._y = Interval( top, bot, ystep )


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
            return self._x.delta / self._y.delta
        elif ( name == 'bottom' ) or ( name == 'b' ):
            return self._y.stop
        elif ( name == 'delta' ) or ( name == 'd' ):
            return self._dmake( self._x.delta, self._y.delta )
        elif ( name == 'deltax' ) or ( name == 'dx' ):
            return self._x.delta
        elif ( name == 'deltay' ) or ( name == 'dy' ):
            return self._y.delta
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

        Note: Linear map coefficients are given as two-tuples or Line named
        tuples where the first item is the straight-line slope, and the second
        item is the straight-line intercept.

        @param horizontal Linear map coefficients from horizontal coordinates
                          from an source plane to a target plane.  When not
                          specified, the map defaults to a 1:1 scaled map with
                          matching origins.
        @param vertical   Same as `horizontal`, but for the vertical axis
        """
        if horizontal is None:
            self.horizontal = Line( 1.0, 0.0 )
        else:
            self.horizontal = Line( *horizontal )
        if vertical is None:
            self.vertical = Line( 1.0, 0.0 )
        else:
            self.vertical = Line( *vertical )


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
        target_x = self.horizontal.a * point.x + self.horizontal.b
        target_y = self.vertical.a   * point.y + self.vertical.b
        if nearx:
            target_x = int( round( target_x ) )
        if neary:
            target_y = int( round( target_y ) )
        return Point( target_x, target_y )


