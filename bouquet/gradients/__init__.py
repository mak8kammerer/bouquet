'''
Gradients
=========

This module provides various types of gradients. Currently,
only linear and radial gradients are supported. Other
types of gradients will be added later.

.. note::

    Note that you should import `bouquet.gradients` module
    in Python script to use gradients in KvLang.

'''

from .linear import LinearGradient
from .radial import RadialGradient

__all__ = ('LinearGradient', 'RadialGradient', )
