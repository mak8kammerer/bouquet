Examples
========

Let me remind you that you can run a demo application showcasing all 
widgets from this library by executing the following command in the 
terminal: 

.. code-block:: bash

    python3 -m bouquet

(replace ``python3`` with ``python``, if you use Windows).

Gradients examples
++++++++++++++++++

:class:`bouquet.gradients.LinearGradient` example (pure Python):

.. code-block:: python

    from kivy.app import App
    from kivy.lang import Builder

    from bouquet.gradients import ColorStop, LinearGradient

    class MyApp(App):

        def build(self):
            return LinearGradient(
                color_stops=[
                    ColorStop(position=0.0, color='red'),
                    ColorStop(position=1.0, color='yellow')
                ],
                angle=60
            )

    if __name__ == '__main__':
        MyApp().run()

:func:`bouquet.gradients.LinearGradient.render_texture` example (pure Python):

.. code-block:: python

    from kivy.app import App
    from kivy.graphics import Ellipse
    from kivy.uix.widget import Widget

    from bouquet.gradients import ColorStop, LinearGradient

    class EllipseWithRadialGradient(Widget):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.color_stops = [
                ColorStop(position=0.0, color='red'),
                ColorStop(position=1.0, color='yellow')
            ]
            self.angle = 60
            with self.canvas:
                self.ellipse = Ellipse(
                    pos=self.pos,
                    size=self.size,
                    texture=LinearGradient.render_texture(
                        size=self.size,
                        color_stops=self.color_stops,
                        angle=self.angle
                    )
                )

        def on_size(self, widget, size):
            self.ellipse.size = size
            self.ellipse.texture = LinearGradient.render_texture(
                size=self.size,
                color_stops=self.color_stops,
                angle=self.angle
            )

    class MyApp(App):

        def build(self):
            return EllipseWithLinearGradient()

    if __name__ == '__main__':
        MyApp().run()

:class:`bouquet.gradients.RadialGradient` example (Python with KVlang):

.. code-block:: python

    from kivy.app import App
    from kivy.lang import Builder

    import bouquet.gradients

    KV = '''
    #: import ColorStop bouquet.gradients.ColorStop
    RadialGradient:
        color_stops: [ \
            ColorStop(position=0.0, color='pink'), \
            ColorStop(position=1.0, color='purple'), \
        ]
    '''

    class MyApp(App):

        def build(self):
            return Builder.load_string(KV)

    if __name__ == '__main__':
        MyApp().run()

:func:`bouquet.gradients.RadialGradient.render_texture` example (Python with KVlang):

.. code-block:: python

    from kivy.app import App
    from kivy.lang import Builder

    KV = '''
    #: import ColorStop bouquet.gradients.ColorStop
    #: import RadialGradient bouquet.gradients.RadialGradient
    Widget:
        canvas:
            Ellipse:
                pos: self.pos
                size: self.size
                texture: RadialGradient.render_texture( \
                    size=self.size, \
                    color_stops=[ \
                        ColorStop(position=0.0, color='pink'), \
                        ColorStop(position=1.0, color='purple'), \
                    ], \
                )
    '''

    class MyApp(App):

        def build(self):
            return Builder.load_string(KV)

    if __name__ == '__main__':
        MyApp().run()

:class:`bouquet.gradients.BilinearGradient` example (pure Python):

.. code-block:: python

    from kivy.app import App
    from bouquet.gradients import BilinearGradient

    class MyApp(App):

        def build(self):
            return BilinearGradient(
                top_left_color='purple',
                top_right_color='purple',
                bottom_left_color='orange',
                bottom_right_color='orange',
            )

    if __name__ == '__main__':
        MyApp().run()

:func:`bouquet.gradients.BilinearGradient.render_texture` example (Python with KVlang):

.. code-block:: python

    from kivy.app import App
    from kivy.lang import Builder

    KV = '''
    #: import BilinearGradient bouquet.gradients.BilinearGradient
    Widget:
        canvas:
            Color:
                rgb: 1.0, 1.0, 1.0
            Ellipse:
                pos: self.pos
                size: self.size
                texture: BilinearGradient.render_texture( \
                    size=self.size, \
                    top_left_color='purple', \
                    top_right_color='purple', \
                    bottom_left_color='orange', \
                    bottom_right_color='orange' \
                )
    '''

    class MyApp(App):

        def build(self):
            return Builder.load_string(KV)

    if __name__ == '__main__':
        MyApp().run()

:class:`bouquet.gradients.ConicalGradient` example (Python with KVlang):

.. code-block:: python

    from kivy.app import App
    from kivy.lang import Builder

    import bouquet.gradients

    KV = '''
    #: import ColorStop bouquet.gradients.ColorStop
    ConicalGradient:
        color_stops: [ \
            ColorStop(position=0.0, color='#e66465'), \
            ColorStop(position=1.0, color='#9198e5'), \
        ]
    '''

    class MyApp(App):

        def build(self):
            return Builder.load_string(KV)

    if __name__ == '__main__':
        MyApp().run()

:func:`bouquet.gradients.ConicalGradient.render_texture` example (pure Python):

.. code-block:: python

    from kivy.app import App
    from kivy.graphics import Ellipse
    from kivy.uix.widget import Widget

    from bouquet.gradients import ColorStop, ConicalGradient

    class EllipseWithRadialGradient(Widget):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.color_stops = [
                ColorStop(position=0.0, color='#e66465'),
                ColorStop(position=1.0, color='#9198e5')
            ]
            with self.canvas:
                self.ellipse = Ellipse(
                    pos=self.pos,
                    size=self.size,
                    texture=ConicalGradient.render_texture(
                        size=self.size,
                        color_stops=self.color_stops,
                    )
                )

        def on_size(self, widget, size):
            self.ellipse.size = size
            self.ellipse.texture = ConicalGradient.render_texture(
                size=self.size,
                color_stops=self.color_stops,
            )

    class MyApp(App):

        def build(self):
            return EllipseWithConicalGradient()

    if __name__ == '__main__':
        MyApp().run()
