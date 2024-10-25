'''
Base module for linear gradient.
'''

__all__ = ('LinearGradient', )

from math import sin, cos, radians

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.graphics import Callback, RenderContext
from kivy.graphics.fbo import Fbo
from kivy.graphics.texture import Texture
from kivy.graphics.transformation import Matrix
from kivy.properties import NumericProperty

# Make sure that OpenGL context is created
import kivy.core.window

from .base import GradientBase, enable_copy_blending, disable_copy_blending


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


VERTEX_SHADER = '''
$HEADER$

uniform mat4 gradientMatrix;

void main() {
    frag_color = color * vec4(1.0, 1.0, 1.0, opacity);
    vec4 tex_coord = (gradientMatrix * vec4(vTexCoords0 * 2.0 - 1.0, 0.0, 1.0));
    tex_coord0 = (tex_coord.xy + 1.0) * 0.5;
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
            Callback(enable_copy_blending)
            LinearGradient(size=(width, height), **kwargs).canvas
            Callback(disable_copy_blending)
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

        width, height = self.size
        length = abs(width * sin(angle)) + abs(height * cos(angle))

        matrix = Matrix()
        matrix = matrix.multiply(Matrix().scale(1.0, height / width, 1.0))
        matrix = matrix.multiply(Matrix().rotate(rotation, 0.0, 0.0, 1.0))
        matrix = matrix.multiply(Matrix().scale(width / length, 1.0, 1.0))
        self.canvas['gradientMatrix'] = matrix.transpose()


Builder.load_string(KV)
Factory.register('LinearGradient', cls=LinearGradient)
