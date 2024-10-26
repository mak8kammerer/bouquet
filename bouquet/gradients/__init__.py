'''
``bouquet.gradients`` module provides various types of gradients.

.. note::
    ``bouquet.gradients`` API is stable and won't change dramatically.

How to use gradients with Vertex Instructions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is possible to use gradient textures with Vertex Instructions via the
``***Gradient.render_texture()`` function. You can take a look at code examples
in the :ref:`Examples` section.
'''

from .base import ColorStop
from .linear import LinearGradient
from .bilinear import BilinearGradient
from .radial import RadialGradient
from .conical import ConicalGradient

__all__ = (
    'ColorStop', 'LinearGradient', 'BilinearGradient',
    'RadialGradient', 'ConicalGradient'
)
