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
'''

from .linear import LinearGradient
from .radial import RadialGradient

__all__ = ('LinearGradient', 'RadialGradient', )
