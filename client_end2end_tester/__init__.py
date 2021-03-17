"""
client_end2end_tester - Python testing for clients against real servers
"""

# There are submodules, but users shouldn't need to know about them.
# Importing just this module is enough.

from __future__ import absolute_import, print_function
from ._version import __version__  # noqa: F401
from ._srvdef import *  # noqa: F403,F401
from ._srvdeffile import *  # noqa: F403,F401
