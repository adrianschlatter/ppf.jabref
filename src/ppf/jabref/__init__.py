"""
ppf.jabref
++++++

"""
try:
    from importlib_metadata import version
except ImportError:                                     # pragma: no cover
    from importlib.metadata import version              # pragma: no cover

# import every function, class, etc. that should be visible in the package
from .jabref import *

__version__ = version(__name__)

del jabref
del utils
