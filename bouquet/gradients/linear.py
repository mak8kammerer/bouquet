'''
Base module for linear gradient.
'''

__all__ = ('LinearGradient', )

from math import sin, cos, radians

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.graphics import Callback, RenderContext
from kivy.graphics.fbo import Fbo
from kivy.graphics.opengl import glBlendFunc, glBlendFuncSeparate, \
                                    GL_ZERO, GL_ONE_MINUS_SRC_ALPHA, \
                                    GL_SRC_ALPHA, GL_ONE
from kivy.graphics.texture import Texture
from kivy.graphics.transformation import Matrix
from kivy.properties import NumericProperty

# Make sure that OpenGL context is created
import kivy.core.window

from .base import GradientBase


KV = '''
<LinearGradient>:
    _y_uv: self.height / self.width
    canvas:
        Color:
            rgba: 1.0, 1.0, 1.0, 1.0
        BindTexture:
            index: 1
            texture: self._1d_gradient_texture
        Mesh:
            vertices: [ \
                self.x + self.width, self.y,                1.0,  self._y_uv, \
                self.x,              self.y,               -1.0,  self._y_uv, \
                self.x + self.width, self.y + self.height,  1.0, -self._y_uv, \
                self.x,              self.y + self.height, -1.0, -self._y_uv, \
            ]
            indices: [0, 1, 2, 3]
            mode: 'triangle_strip'
'''


VERTEX_SHADER = '''
$HEADER$

uniform mat4 gradientMatrix;

void main() {
    frag_color = color * vec4(1.0, 1.0, 1.0, opacity);
    vec2 tex_coord = (gradientMatrix * vec4(vTexCoords0, 0.0, 1.0)).xy;
    tex_coord0 = (tex_coord + 1.0) * 0.5;
    gl_Position = projection_mat * modelview_mat * vec4(vPosition, 0.0, 1.0);
}
'''


FRAGMENT_SHADER = '''
$HEADER$

uniform sampler2D gradientTexture;

void main() {
    gl_FragColor = frag_color * texture2D(gradientTexture, tex_coord0);
}
'''


class LinearGradient(GradientBase):
    '''
    The LinearGradient class provides a way to create linear gradients in Kivy.

    A linear gradient is a visual effect where color is linearly interpolated
    between multiple color stops (:class:`ColorStop`) across a straight line,
    known as the gradient line.

    .. seealso::
        Note, a linear gradient is rendered as described in the
        `CSS specification
        <https://www.w3.org/TR/css-images-3/#linear-gradients>`_.
    '''

    _y_uv = NumericProperty()

    angle = NumericProperty()
    '''
    Defines the rotation of the gradient line in degrees. The angle determines
    the direction in which the gradient will be rendered, where 0 degrees
    represents a vertical gradient (from bottom to top), and 90 degrees
    represents a horizontal gradient (from left to right).

    :attr:`angle` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    '''

    @staticmethod
    def render_texture(**kwargs) -> Texture:
        '''
        Renders gradient at FBO and returns the texture.

        :param kwargs:
            Any :class:`LinearGradient` properties.
        '''
        width = kwargs.pop('width', 100)
        height = kwargs.pop('height', 100)
        width, height = kwargs.pop('size', (width, height))

        fbo = Fbo(size=(width, height))
        with fbo:
            Callback(
                lambda arg: glBlendFunc(GL_ONE, GL_ZERO)
            )
            # _y_uv is not calculated automatically
            LinearGradient(
                _y_uv=(height / width),
                size=(width, height),
                **kwargs
            ).canvas
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
        self.fbind('size', self._update_gradient_matrix)
        self.fbind('angle', self._update_gradient_matrix)
        super(LinearGradient, self).__init__(**kwargs)

    def _update_gradient_matrix(self, _, __):
        angle = radians(self.angle)
        rotation = angle - radians(90)

        length = abs(self.width * sin(angle)) + abs(self.height * cos(angle))
        scale = self.width / length

        matrix = Matrix()
        matrix = matrix.multiply(Matrix().rotate(rotation, 0.0, 0.0, 1.0))
        matrix = matrix.multiply(Matrix().scale(scale, 1.0, 1.0))
        self.canvas['gradientMatrix'] = matrix.transpose()


Builder.load_string(KV)
Factory.register('LinearGradient', cls=LinearGradient)
