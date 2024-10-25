'''
Base module for conical gradient.
'''

__all__ = ('ConicalGradient', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.graphics import Callback, RenderContext
from kivy.graphics.fbo import Fbo
from kivy.graphics.opengl import glBlendFunc, glBlendFuncSeparate, \
                                    GL_ZERO, GL_ONE_MINUS_SRC_ALPHA, \
                                    GL_SRC_ALPHA, GL_ONE
from kivy.graphics.texture import Texture
from kivy.graphics.transformation import Matrix
from kivy.properties import NumericProperty, ReferenceListProperty

# Make sure that OpenGL context is created
import kivy.core.window

from .base import GradientBase


KV = '''
<ConicalGradient>:
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


VERTEX_SHADER = '''
$HEADER$

uniform mat4 gradientMatrix;

void main() {
    frag_color = color * vec4(1.0, 1.0, 1.0, opacity);
    tex_coord0 = (gradientMatrix * vec4(vTexCoords0 * 2.0 - 1.0, 0.0, 1.0)).xy;
    gl_Position = projection_mat * modelview_mat * vec4(vPosition, 0.0, 1.0);
}
'''


FRAGMENT_SHADER = '''
$HEADER$

uniform sampler2D gradientTexture;

void main() {
    float result = atan(-tex_coord0.y, -tex_coord0.x) * 0.15915494309188485 + 0.5;
    gl_FragColor = texture(gradientTexture, vec2(result, 0.5));
}
'''


class ConicalGradient(GradientBase):
    '''
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

    @staticmethod
    def render_texture(**kwargs) -> Texture:
        '''
        Renders gradient at FBO and returns the texture.

        :param kwargs:
            Any :class:`ConicalGradient` properties.
        '''
        width = kwargs.pop('width', 100)
        height = kwargs.pop('height', 100)
        width, height = kwargs.pop('size', (width, height))

        fbo = Fbo(size=(width, height))
        with fbo:
            Callback(
                lambda arg: glBlendFunc(GL_ONE, GL_ZERO)
            )
            ConicalGradient(size=(width, height), **kwargs).canvas
            Callback(
                lambda arg: glBlendFuncSeparate(
                    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE
                )
            )
        fbo.draw()
        return fbo.texture
    
    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            vs=VERTEX_SHADER,
            fs=FRAGMENT_SHADER,
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True
        )
        self.canvas['gradientTexture'] = 1
        self.fbind('size',                self._update_gradient_matrix)
        self.fbind('gradient_center_pos', self._update_gradient_matrix)
        super(ConicalGradient, self).__init__(**kwargs)
    
    def _update_gradient_matrix(self, _, __):
        scale = self.width / self.height
        x = self.gradient_center_x * 2.0 - 1.0
        y = self.gradient_center_y * 2.0 - 1.0
        x *= scale

        matrix = Matrix()
        matrix = matrix.multiply(Matrix().translate(-x, -y, 0.0))
        matrix = matrix.multiply(Matrix().scale(scale, 1.0, 1.0))

        self.canvas['gradientMatrix'] = matrix


Builder.load_string(KV)
Factory.register('ConicalGradient', cls=ConicalGradient)
