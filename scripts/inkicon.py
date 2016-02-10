#!/usr/bin/env python3
#=============================================================================
#
# Creates .ico Icon Files from SVG Images
#
#=============================================================================

"""
Creates .ico Icon Files from SVG Images
=======================================

This script makes use of [Inkscape](http://inkscape.org/) and ImageMagick.
The paths at the top of the file allow you to change the location of these
programs per your installation.

The icon that is produced contains multiple resolutions to maintain fidelity
at all common uses for icons on a Windows desktop.

The source SVG document should use a page layout with square dimensions.  The
way Inkscape is used, the document's page is used as the source area of the
icon.
"""


import os
import re
import subprocess
import sys


__version__ = '0.0.0'


#=============================================================================
# Try not to rely on the user having their path set up. Adjust as needed.
INKSCAPE = '/cygdrive/d/Program Files (x86)/Inkscape/inkscape.exe'
CONVERT  = '/usr/bin/convert'


#=============================================================================
def export( filename, width = 128, height = 128, png = None ):
    """
    Exports the given SVG file at the requested dimensions.
    """
    if os.path.isfile( filename ) == False:
        raise IOError(
            'Unable to locate source SVG file at "{}"'.format( filename )
        )
    if png is None:
        png = re.sub(
            r'\.svg$',
            '{}x{}.png'.format( width, height ),
            filename
        )
    command = [
        INKSCAPE,
        filename,
        '--export-area-page',
        '--export-height={}'.format( height ),
        '--export-width={}'.format( width ),
        '--export-png={}'.format( png ),
    ]
    return subprocess.call( command )


#=============================================================================
def export_set( filename ):
    """
    Exports an SVG to a set of PNGs for use in building an ICO file.
    """
    sizes = [ 128, 64, 48, 32, 24, 16 ]
    pngs  = []
    for size in sizes:
        png    = re.sub( r'\.svg$', 'tmp{}.png'.format( size ), filename )
        result = export( filename, size, size, png )
        if result != 0:
            for png in pngs:
                os.unlink( png )
            raise RuntimeError( 'Failed to rasterize image.' )
        pngs.append( png )
    return pngs


#=============================================================================
def make_ico( filename, ico = None ):
    """
    Creates an ICO file using ImageMagick.
    """
    if ico is None:
        ico = re.sub( r'\.svg$', '.ico', filename )
    pngs = export_set( filename )
    command = [ CONVERT ]
    command.extend( pngs )
    command.append( ico )
    result = subprocess.call( command )
    for png in pngs:
        os.unlink( png )


#=============================================================================
def main( argv ):
    """
    Script execution entry point

    @param argv List of arguments passed to the script
    @return     Shell exit code (0 = success)
    """

    # imports when using this as a script
    import argparse

    # create and configure an argument parser
    parser = argparse.ArgumentParser(
        description = 'Creates .ico Icon Files from SVG Images',
        add_help    = False
    )
    parser.add_argument(
        '-h',
        '--help',
        default = False,
        help    = 'Display this help message and exit.',
        action  = 'help'
    )
    parser.add_argument(
        '-v',
        '--version',
        default = False,
        help    = 'Display script version and exit.',
        action  = 'version',
        version = __version__
    )
    parser.add_argument(
        'source',
        help = 'The source SVG file.'
    )

    # parse the arguments
    args = parser.parse_args( argv[ 1 : ] )

    # make the .ico file from the .svg file
    result = make_ico( args.source )

    # return result
    return result


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )

