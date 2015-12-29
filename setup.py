#=============================================================================
#
# hzgfx Package Setup Script
#
# ### Normal Installation
#
#     python setup.py install
#
# ### Development Installation (symlinks to current copy)
#
#     python setup.py develop
#
# ### Create a Compressed Source Distribution
#
#     python setup.py sdist
#
#=============================================================================

"""
hzgfx Package Setup Script
=============================

Run this script to install the screener package for your system.

    python setup.py install

"""


from setuptools import setup


setup(
    name         = 'hzgfx',
    version      = '0.0.0',
    description  = 'Graphics Programming Tools',
    url          = 'https://github.com/zhester/hzgfx',
    author       = 'Zac Hester',
    author_email = 'zac.hester@gmail.com',
    license      = 'BSD',
    packages     = [ 'hzgfx' ],
    zip_safe     = False
)


