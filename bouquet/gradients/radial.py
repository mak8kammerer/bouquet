'''
Base module for radial gradient.
'''

__all__ = ('RadialGradient', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.graphics import RenderContext, Fbo
from kivy.graphics.texture import Texture

# Make sure that OpenGL context is created
import kivy.core.window

from .base import GradientBase


KV = '''
<RadialGradient>:
    canvas:
        Color:
            rgba: 1.0, 1.0, 1.0, 1.0
        BindTexture:
            index: 1
            texture: self._1d_gradient_texture
        Rectangle:
            pos: self.pos
            size: self.size
'''


FRAGMENT_SHADER = '''
$HEADER$

uniform sampler2D gradientTexture;

void main() {
    float distance = distance(tex_coord0, vec2(0.5)) * 2.0;
    gl_FragColor = texture2D(gradientTexture, vec2(distance, 0.5));
}
'''


class RadialGradient(GradientBase):
    '''
    Widget for creating a radial gradient effect, in which color is linearly
    interpolated from the center to the edges of the widget.
    '''

    @staticmethod
    def render_texture(**kwargs) -> Texture:
        '''
        Renders gradient at FBO and returns the texture.

        :param kwargs:
            Any :class:`RadialGradient` properties.
        '''
        width = kwargs.pop('width', 100)
        height = kwargs.pop('height', 100)
        width, height = kwargs.pop('size', (width, height))

        fbo = Fbo(size=(width, height))
        with fbo:
            RadialGradient(size=(width, height), **kwargs).canvas
        fbo.draw()
        return fbo.texture

    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            fs=FRAGMENT_SHADER,
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True
        )
        self.canvas['gradientTexture'] = 1
        super(RadialGradient, self).__init__(**kwargs)


Builder.load_string(KV)
Factory.register('RadialGradient', cls=RadialGradient)
