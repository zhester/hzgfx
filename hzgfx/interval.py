#=============================================================================
#
# Linear Numeric Intervals
#
#=============================================================================

"""
Linear Numeric Intervals
========================
"""


__version__ = '0.0.0'


#=============================================================================
def interval( *args, **kwargs ):
    """
    Factory function to automate different ways of creating Interval objects.

    Initializing arguments are flexible depending on the number and types of
    each.  The following list describes each in order of position.  When no
    arguments are given, the `None` option for the first parameter is assumed.

    @param 0
        `None` creates an interval over [ 0.0, 1.0 ]
        Integers create an interval over [ 0, args[0] )
        Floating-point numbers create an interval over [ 0.0, args[0] ]
        A sequence of values is used as constructor arguments to either
        `Interval` or `RealInterval`.  A `RealInterval` is used if any of the
        values in the sequence is a floating-point number.
    @param 1
        If argument 0 is numeric, this argument is used as the upper limit of
        the interval.
    @param 2
        If argument 0 is numeric, this argument is used as the step value of
        the interval.
    @return
        An Interval object with the requested properties.
    """

    # Check for no arguments given or a `None` argument.
    if ( len( args ) == 0 ) or ( args[ 0 ] is None ):
        return RealInterval( 1.0 )

    # Check for a sequence argument.
    if isinstance( args[ 0 ], ( tuple, list ) ):

        # See if there is a float in the sequence.
        if any( type( v ) is float for v in args[ 0 ] ) == True:
            return RealInterval( *args[ 0 ][ : 3 ] )

        # No floats in sequence.
        else:
            return Interval( *args[ 0 ][ : 3 ] )

    # Set the default constructor arguments.
    start = args[ 0 ]
    stop  = None if len( args ) <= 1 else args[ 1 ]
    step  = 1    if len( args ) <= 2 else args[ 2 ]

    # Determine what kind of interval to create.
    if any( type( v ) is float for v in args ) == True:
        itype = RealInterval
    else:
        itype = Interval

    # Construct the requested interval.
    return itype( start, stop, step )


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

