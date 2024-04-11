'''
Base module for radial gradient.
'''

__all__ = ('RadialGradient', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.graphics import RenderContext, Fbo
from kivy.properties import ColorProperty

# Make sure that OpenGL context is created
import kivy.core.window


KV = '''
<RadialGradient>:
    canvas:
        Color:
            rgba: 1.0, 1.0, 1.0, 1.0
        Rectangle:
            pos: self.pos
            size: self.size
'''


FRAGMENT_SHADER = '''
$HEADER$

// Based on https://gist.github.com/tito/4250317#file-gpuradialgradient-py

uniform vec4 centerColor;
uniform vec4 borderColor;

void main() {
    float distance = distance(tex_coord0, vec2(0.5)) * 2.0;
    gl_FragColor = mix(centerColor, borderColor, distance);
}
'''


class RadialGradient(Widget):
    '''
    Widget for creating a radial gradient effect, in which color is linearly
    interpolated from the center to the edges of the widget.

    Currently, it is possible to set only two colors: the color of the center
    (:attr:`center_color`) and the color of the border (:attr:`border_color`).
    '''

    center_color = ColorProperty(defaultvalue='white')
    '''
    Color of the widget center.

    :attr:`center_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `white`.
    '''

    border_color = ColorProperty(defaultvalue='black')
    '''
    Color of the widget borders.

    :attr:`border_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `black`.
    '''

    @staticmethod
    def render_texture(**kwargs):
        '''
        Renders gradient at Fbo and returns the texture.

        :param kwargs:
            Any :class:`RadialGradient` properties.
        '''
        fbo = Fbo(size=kwargs.get('size', (100, 100)))
        with fbo:
            RadialGradient(**kwargs).canvas
        fbo.draw()
        return fbo.texture

    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            fs=FRAGMENT_SHADER,
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True
        )

        canvas = self.canvas
        canvas['centerColor'] = tuple(self.center_color)
        canvas['borderColor'] = tuple(self.border_color)

        fbind = self.fbind
        callback = self._set_color
        fbind('center_color', callback, uniform_name='centerColor')
        fbind('border_color', callback, uniform_name='borderColor')

        super(RadialGradient, self).__init__(**kwargs)

    def _set_color(self, widget, value, uniform_name=None):
        if uniform_name is not None:
            widget.canvas[uniform_name] = tuple(value)


Builder.load_string(KV)
Factory.register('RadialGradient', cls=RadialGradient)
