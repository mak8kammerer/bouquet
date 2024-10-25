'''
Base module for radial gradient.
'''

__all__ = ('RadialGradient', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.graphics import Callback, RenderContext
from kivy.graphics.fbo import Fbo
from kivy.graphics.opengl import glBlendFunc, glBlendFuncSeparate, \
                                    GL_ZERO, GL_ONE_MINUS_SRC_ALPHA, \
                                    GL_SRC_ALPHA, GL_ONE
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, ReferenceListProperty

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

uniform vec2      gradientCenter;
uniform float     gradientRadius;
uniform sampler2D gradientTexture;

void main() {
    float distance = distance(tex_coord0, gradientCenter) * gradientRadius;
    // workaround: when the radius equals 0.0, add 1.0 to the distance (0.0)
    distance += step(gradientRadius, 0.0);
    gl_FragColor = frag_color * texture2D(gradientTexture, vec2(distance, 0.5));
}
'''


class RadialGradient(GradientBase):
    '''
    The RadialGradient class provides a way to create radial gradients in Kivy.

    A radial gradient is a visual effect where color is linearly interpolated
    between multiple color stops (:class:`ColorStop`) from the center to the
    border.

    .. hint::
        The value 0.0 of :attr:`ColorStop.position` represents the center,
        while 1.0 represents the border.
    '''

    gradient_center_x = NumericProperty(defaultvalue=0.5)
    '''
    X-coordinate of the gradient's center, where 0.0 corresponds
    to the left edge of the widget and 1.0 to the right edge.

    :attr:`gradient_center_x` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.5`.
    '''

    gradient_center_y = NumericProperty(defaultvalue=0.5)
    '''
    Y-coordinate of the gradient's center, where 0.0 corresponds
    to the top edge of the widget and 1.0 to the bottom edge.

    :attr:`gradient_center_y` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.5`.
    '''

    gradient_center_pos = ReferenceListProperty(
        gradient_center_x, gradient_center_y
    )
    '''
    Position of the gradient center.

    :attr:`gradient_center_pos` is a
    :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`gradient_center_x`, :attr:`gradient_center_y`) properties.
    '''

    radius = NumericProperty(defaultvalue=1.0)
    '''
    Radius of the gradient. A larger value extends the gradient
    effect, while a smaller value contracts it.

    :attr:`radius` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `1.0`.
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
            Callback(
                lambda arg: glBlendFunc(GL_ONE, GL_ZERO)
            )
            RadialGradient(size=(width, height), **kwargs).canvas
            Callback(
                lambda arg: glBlendFuncSeparate(
                    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE
                )
            )
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
        canvas['gradientTexture'] = 1
        canvas['gradientRadius'] = 2.0
        canvas['gradientCenter'] = (0.5, 0.5)

        fbind = self.fbind
        fbind('radius',              self._update_gradient_radius)
        fbind('gradient_center_pos', self._update_gradient_center)
        super(RadialGradient, self).__init__(**kwargs)

    def _update_gradient_center(self, _, value):
        self.canvas['gradientCenter'] = tuple(value)

    def _update_gradient_radius(self, _, value):
        radius = 0.0 if value <= 0.0 else (1.0 / value) * 2.0
        self.canvas['gradientRadius'] = radius


Builder.load_string(KV)
Factory.register('RadialGradient', cls=RadialGradient)
