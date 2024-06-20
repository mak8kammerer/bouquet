'''
Base module for linear gradient.
'''
# TODO: optimizations

__all__ = ('LinearGradient', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.graphics import RenderContext
from kivy.properties import NumericProperty

from .base import GradientBase


KV = '''
<LinearGradient>:
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

uniform float     angle;
uniform sampler2D gradientTexture;

void main() {
    gl_FragColor = texture2D(gradientTexture, vec2(tex_coord0.x, 0.5));
}
'''


class LinearGradient(GradientBase):
    '''
    '''

    angle = NumericProperty(defaultvalue=90)
    '''
    '''

    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            fs=FRAGMENT_SHADER,
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True
        )
        self.canvas['gradientTexture'] = 1
        self.fbind('angle', self._update_angle)
        super(LinearGradient, self).__init__(**kwargs)

    def _update_angle(self, widget, angle):
        widget.canvas['angle'] = angle


Builder.load_string(KV)
Factory.register('LinearGradient', cls=LinearGradient)
