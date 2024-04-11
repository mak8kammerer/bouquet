'''
`bouquet.gradients` module provides various types of gradients.
Currently, only linear (:class:`LinearGradient`) and radial
(:class:`RadialGradient`) gradients are supported. Other types of
gradients will be added later.

Examples
~~~~~~~~

:class:`LinearGradient`:

.. code-block:: python

    from kivy.app import App
    from bouquet.gradients import LinearGradient

    class MyApp(App):

        def build(self):
            return LinearGradient(
                top_left_color='purple',
                top_right_color='purple',
                bottom_left_color='orange',
                bottom_right_color='orange',
            )

    MyApp().run()

:class:`RadialGradient`:

.. code-block:: python

    from kivy.app import App
    from kivy.lang import Builder

    import bouquet.gradients

    KV = """
    RadialGradient:
        center_color: (1.0, 0.0, 0.0, 1.0)
        border_color: (1.0, 0.0, 0.0, 0.0)
    """

    class MyApp(App):

        def build(self):
            return Builder.load_string(KV)

     MyApp().run()

Textures
~~~~~~~~

This is possible to use gradient textures with Vertex Instructions via the
`render_texture()` function.

Pure Python example:

.. code-block:: python

    from kivy.app import App
    from kivy.graphics import Ellipse
    from kivy.uix.widget import Widget

    from bouquet.gradients import LinearGradient

    class EllipseWithGradient(Widget):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas:
                self.ellipse = Ellipse(
                    pos=self.pos,
                    size=self.size,
                    texture=LinearGradient.render_texture(size=self.size)
                )

        def on_size(self, widget, size):
            self.ellipse.size = size
            self.ellipse.texture = LinearGradient.render_texture(size=size)

    class MyApp(App):

        def build(self):
            return EllipseWithGradient()

    MyApp().run()

Example with KvLang:

.. code-block:: python

    from kivy.app import App
    from kivy.lang import Builder

    KV = """
    #: import LinearGradient bouquet.gradients.LinearGradient
    Widget:
        canvas:
            Color:
                rgb: 1.0, 1.0, 1.0
            Ellipse:
                pos: self.pos
                size: self.size
                texture: LinearGradient.render_texture(size=self.size)
    """

    class MyApp(App):

        def build(self):
            return Builder.load_string(KV)

    MyApp().run()
'''

from .linear import LinearGradient
from .radial import RadialGradient

__all__ = ('LinearGradient', 'RadialGradient', )
