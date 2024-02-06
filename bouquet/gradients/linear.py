'''
Base module for linear gradient.
'''
# TODO: implement alternative color spaces

__all__ = ('LinearGradient', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.graphics import RenderContext
from kivy.properties import ColorProperty
from kivy.uix.anchorlayout import AnchorLayout

# Make sure that OpenGL context is created
import kivy.core.window


KV = '''
<LinearGradient>:
    canvas:
        Color:
            rgba: 1.0, 1.0, 1.0, 1.0
        Rectangle:
            pos: self.pos
            size: self.size
'''


FRAGMENT_SHADER = '''
$HEADER$

uniform vec4 topLeftColor;
uniform vec4 topRightColor;
uniform vec4 bottomLeftColor;
uniform vec4 bottomRightColor;

void main() {
    vec4 topColor = mix(topLeftColor, topRightColor, tex_coord0.x);
    vec4 bottomColor = mix(bottomLeftColor, bottomRightColor, tex_coord0.x);
    gl_FragColor = mix(topColor, bottomColor, tex_coord0.y);
}
'''


class LinearGradient(AnchorLayout):
    '''
    The `LinearGradient` is a Kivy widget for creating a linear gradient
    background with customizable colors for each corner.

    Note that `LinearGradient` is an `AnchorLayout` subclass, so you can put
    any widget inside it.
    '''

    top_left_color = ColorProperty(defaultvalue='green')
    '''
    Color of the top left corner of gradient.

    :attr:`top_left_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `green`.
    '''

    bottom_left_color = ColorProperty(defaultvalue='black')
    '''
    Color of the top bottom corner of gradient.

    :attr:`bottom_left_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `black`.
    '''

    top_right_color = ColorProperty(defaultvalue='yellow')
    '''
    Color of the top right corner of gradient.

    :attr:`top_right_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `yellow`.
    '''

    bottom_right_color = ColorProperty(defaultvalue='red')
    '''
    Color of the bottom right corner of gradient.

    :attr:`bottom_right_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `red`.
    '''

    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            fs=FRAGMENT_SHADER,
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True
        )
        self.canvas['topLeftColor'] = tuple(self.top_left_color)
        self.canvas['topRightColor'] = tuple(self.top_right_color)
        self.canvas['bottomLeftColor'] = tuple(self.bottom_left_color)
        self.canvas['bottomRightColor'] = tuple(self.bottom_right_color)

        super(LinearGradient, self).__init__(**kwargs)

    def on_top_left_color(self, widget, new_value):
        widget.canvas['topLeftColor'] = tuple(new_value)

    def on_bottom_left_color(self, widget, new_value):
        widget.canvas['bottomLeftColor'] = tuple(new_value)

    def on_top_right_color(self, widget, new_value):
        widget.canvas['topRightColor'] = tuple(new_value)

    def on_bottom_right_color(self, widget, new_value):
        widget.canvas['bottomRightColor'] = tuple(new_value)


Builder.load_string(KV)
Factory.register('LinearGradient', cls=LinearGradient)
