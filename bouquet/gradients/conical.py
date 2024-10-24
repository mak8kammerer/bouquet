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
        self.fbind('size', self._update_gradient_matrix)
        super(ConicalGradient, self).__init__(**kwargs)
    
    def _update_gradient_matrix(self, _, __):
        matrix = Matrix().scale(self.width / self.height, 1.0, 1.0)
        self.canvas['gradientMatrix'] = matrix


Builder.load_string(KV)
Factory.register('ConicalGradient', cls=ConicalGradient)
