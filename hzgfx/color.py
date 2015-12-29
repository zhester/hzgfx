#=============================================================================
#
# Color Management
#
#=============================================================================

"""
Color Management
================

This system intends to equally support many different color representation
schemes.  There are many translators built into the `Color` class, and some
attempts are made at automatically converting between representations.

There are two fundamentally different representations:

- `Color` is used to represent typical, 24-bit RGB colors.
- `ColorAlpha` is used to represent modern, 32-bit ARGB or RGBA colors.

For historical purposes, 24-bit colors always use the lower-order bits in
numeric representations.  For interoperability, 32-bit colors use the
high-order bits for the alpha channel, but expect string-style color notation
to list those last (e.g. "#RRGGBBAA").  If your code needs to use integer
values with RGBA channel ordering, you can select all numeric output to use
that format instead.

To limit a lot of repetitious documentation in the code, assume all sequences
of non-alpha color channels occur in the same order: red, green, then blue.

ZIH TODO:

- Implement ColorAlpha
- Implement color arithmetic methods

"""


__version__ = '0.0.0'


#=============================================================================
class Color( object ):
    """
    Base color representational object.
    """


    #=========================================================================
    # Possible string formatting modes

    STR_PLAIN   = 0         # "RRGGBB"
    STR_POUNDS  = 1         # "#RRGGBB"
    STR_POUNDS3 = 2         # "#RGB"
    STR_POUNDS6 = 1         # "#RRGGBB"
    STR_LITERAL = 3         # "0xRRGGBB"


    #=========================================================================
    @staticmethod
    def int2rgb( integer ):
        """
        Converts a color represented by a 24-bit integer value into an RGB
        tuple.

        @param integer A 24-bit integer RGB representation of the color
        @return        A 3-tuple containing the 8-bit integer values for
                       each primary color channel
        """
        return (
            ( ( integer >> 16 ) & 0xFF ),
            ( ( integer >>  8 ) & 0xFF ),
            ( ( integer >>  0 ) & 0xFF )
        )


    #=========================================================================
    @staticmethod
    def rgb2int( rgb, green = None, blue = None ):
        """
        Converts a color represented by an RGB tuple into a 24-bit integer
        value.

        @param rgb   A 3-tuple containing the 8-bit values for each primary
                     color channel;  If `green` and `blue` are specified, this
                     becomes the 8-bit channel value for red.
        @param green Optional 8-bit channel value for green
        @param blue  Optional 8-bit channel value for blue
        @return      The 24-bit integer RGB representation of the color
        """
        if ( green is not None ) and ( blue is not None ):
            return ( ( rgb   & 0xFF ) << 16 ) \
                 | ( ( green & 0xFF ) <<  8 ) \
                 | ( ( blue  & 0xFF ) <<  0 )
        return Color.rgb2int( *rgb )


    #=========================================================================
    def __init__( self, value = 0x00000000 ):
        """
        Initializes a Color object.

        @param value See: value parameter for the `set()` method
        """
        self._int    = 0
        self._rgn    = ( 0, 0, 0 )
        self.strmode = self.STR_POUNDS
        self.set( value )


    #=========================================================================
    def __int__( self ):
        """
        Provides conversion to integer representation.

        @return The integer representation of this color
        """
        return self._int


    #=========================================================================
    def __str__( self ):
        """
        Produces a shorthand hexadecimal string representing the color.

        @return A hexadecimal string representation of the color
        """
        if self.strmode == self.STR_LITERAL:
            return '0x{:06X}'.format( self._int )
        elif self.strmode == self.STR_PLAIN:
            return '{:06X}'.format( self._int )
        elif self.strmode == self.STR_POUNDS3:
            ### ZIH TODO
            return '#{:06X}'.format( self._int )
        else:
            return '#{:06X}'.format( self._int )


    #=========================================================================
    def __tuple__( self ):
        """
        Provides conversion to tuple representation.

        @return The tuple representation of this color
        """
        return self._rgb


    #=========================================================================
    def set( self, value ):
        """
        Set the color using type/format auto-detection.

        @param value A color representation in one of the following formats:
                     - A 24-bit integer representation (8-bits per channel)
                     - A shorthand hexadecimal string representing each color
                       channel as "RGB" or "RRGGBB" with or without a leading
                       pounds symbol or "0x" literal prefix
                     - A list or tuple that represents the color using three
                       items, each an 8-bit integer value for each channel
                     - A mapping type that represents each color channel with
                       the keys 'r' for red, 'g' for green, and 'b' for blue
                     - A generic sequence that begins with three integers
                     - An object that has attributes named 'r', 'g', and 'b'
        """

        # integer color
        if type( value ) is int:
            self._int = value
            self._rgb = self.int2rgb( self._int )

        # string color
        elif isstring( value ):
            val = value.strip( '#' )
            if val.startswith( '0x' ):
                val = val[ 2 : ]
            if len( val ) == 3:
                val = ''.join( c * 2 for c in val )
            self._int = int( val, 16 )
            self._rgb = self.int2rgb( self._int )

        # sequence/mapping with RGB values
        elif hasattr( value, '__getitem__' ):

            # mapping with RGB values
            if hasattr( value, 'keys' ):
                self._rgb = ( value[ 'r' ], value[ 'g' ], value[ 'b' ] )
                self._int = self.rgb2int( self._rgb )

            # any other generic sequence
            else:
                self._rgb = ( value[ 0 ], value[ 1 ], value[ 2 ] )
                self._int = self.rgb2int( self._rgb )

        # an object that appears to contain color information
        elif hasattr( value, 'r' ) \
         and hasattr( value, 'g' ) \
         and hasattr( value, 'b' ):
            self._rgb = ( value.r, value.g, value.b )
            self._int = self.rgb2int( self._rgb )

        # still not sure what this is
        else:

            # try a list or tuple with RGB values
            try:
                len( value )
                value[ 0 : 0 ]
            except TypeError:
                pass
            else:
                self._rgb = tuple( value[ 0 : 3 ] )
                self._int = self.rgb2int( self._rgb )

            # unable to figure out how to set color
            raise TypeError(
                'Unable to use {} value to set color.'.format( type( value ) )
            )


#=============================================================================
def isstring( obj ):
    """
    Wrapper to provide Python 2 and 3 support for string type testing.

    @param obj The object to test to see if it is a string
    @return    True if the object is a string
    """
    try:
        result = isinstance( obj, basestring )
    except NameError:
        result = isinstance( obj, str )
    return result

