#=============================================================================
# coding=utf-8
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
# Scaling is used when the all values from a source interval must be able to
# reach all values in a target interval.  The extremes of the source interval
# map directly to the extremes of the target interval.
#
#     SOURCE := TARGET
#
#     |---------S---------|
#      \                 /
#       \               /
#       |-------T-------|
#
# ### Clipping
#
# Clipping is used when a subset of the source interval must be mapped to all
# values in a target interval.  Values at one or both extremes of the source
# interval do not map to values in the target interval.  These are considered
# "clipped" (missing) from the output.
#
#     SOURCE :⊂ TARGET
#
#     |----+----S----+----|
#         /           \
#        /             \
#       |-------T-------|
#
# ### Filling
#
# Filling provides the opposite functionality of clipping.  Filling is used
# when all values in a source interval must be mapped to a subset of the
# values in a target interval.  Values at one or both extremes of the target
# interval do not map to values in the source interval.  These are considered
# "filled" (possibly with a default value) in the output.
#
#     SOURCE :⊃ TARGET
#
#       |-------S-------|
#        \             /
#         \           /
#     |----+----T----+----|
#
#=============================================================================

"""
Cartesian Coordinate Mapping
============================

### ZIH - Add user documentation.

"""


import collections
import math

import interval


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
class LinearMap( object ):
    """
    Models a linear mapping between two intervals.
    """


    #=========================================================================
    def __init__( self, source, target, clip = None, fill = None ):
        """
        Initializes a LinearMap object.

        @param source The source interval of the mapping
        @param target The target interval of the mapping
        @param clip   Specify the clipping modification interval
        @param fill   Specify the filling modification interval
        @throws       ValueError if one of the intervals has no length
        """

        # Initialize/create/default interval instances.
        self.source = self._interval_argument( source )
        self.target = self._interval_argument( target )

        # Check the intervals to make sure mapping would work.
        if self.source.delta == 0:
            raise ValueError( 'Source interval must have non-zero domain.' )
        if self.target.delta == 0:
            raise ValueError( 'Target interval must have non-zero domain.' )

        # Initialize the clip and fill boundaries.
        self.set_clip( clip )
        self.set_fill( fill )

        # Make sure the mapping function has been initialized.
        self._update()


    #=========================================================================
    def __getitem__( self, point ):
        """
        Supports point translation through subscript notation.

        @param point A point in the source interval
        @return      The corresponding point in the target interval
        """
        return self.translate( point )


    #=========================================================================
    def set_clip( self, clip = None ):
        """
        Sets or clears the clip mapping between intervals.

        @param clip If default or None, disables clipping.
                    If an interval.Interval instance, it is used directly.
                    Otherwise, this is the constructor argument to the
                    interval.interval() factory function.
        @throws     ValueError if the clip region has no size
        """

        # Check for disabled clipping.
        if clip is None:
            self._clip = None
            return

        # Set the clip interval.
        self._clip = self._interval_argument( clip )

        # Sanity check interval.
        if self._clip.delta == 0:
            raise ValueError( 'Unable to use zero-length clipping interval.' )

        # Update the mapping function.
        self._update()


    #=========================================================================
    def set_fill( self, fill = None ):
        """
        Sets or clears the fill mapping between intervals.

        @param fill If default or None, disables filling.
                    If an interval.Interval instance, it is used directly.
                    Otherwise, this is the constructor argument to the
                    interval.interval() factory function.
        @throws     ValueError if the fill region has no size
        """

        # Check for disabled filling.
        if fill is None:
            self._fill = None
            return

        # Set the fill interval.
        self._fill = self._interval_argument( fill )

        # Sanity check interval.
        if self._fill.delta == 0:
            raise ValueError( 'Unable to use zero-length filling interval.' )

        # Update the mapping function.
        self._update()


    #=========================================================================
    def translate( self, point ):
        """
        Translates a point from an independent point on a source axis to a
        dependent point on a target axis.

        @param point A point in the source interval
        @return      The corresponding point in the target interval
        """
        return self._map.a * point + self._map.b


    #=========================================================================
    @staticmethod
    def _interval_argument( argument ):
        """
        Checks any initialization argument and converts it into an interval if
        it isn't one already.

        @param argument The argument to use for initialization
        @return         A usable Interval object
        """

        # Check for instances of Interval.
        if isinstance( argument, interval.Interval ):
            return argument

        # Attempt to use the argument to create an interval.
        return interval.interval( argument )


    #=========================================================================
    def _update( self ):
        """
        Updates the mapping relationship given the current object state.

        The relationship is modified if there is an active clip or fill.
        Otherwise, the default relationship is used.
        """

        # Initially, assume mapping is direct or scaled between intervals.
        startx = self.source.start
        starty = self.target.start
        deltax = self.source.delta
        deltay = self.target.delta

        # Check for a clipping interval.
        if self._clip is not None:

            # Adjust mapping values to clip.
            starty = self._clip.start
            deltay = self._clip.delta

        # Check for a filling interval.
        if self._fill is not None:

            # Adjust mapping values to fill.
            startx = self._fill.start
            deltax = self._fill.delta

        # Compute mapping coefficients.
        a = deltay / float( deltax )
        b = starty - a * startx
        self._map = Line( a, b )


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
        self._x = interval.Interval( left, right, xstep )
        self._y = interval.Interval( top, bot, ystep )


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
        return 'X := {} / Y := {}'.format( self._x, self._y )


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


