'''
Base module for gradients with color stops.
'''
# TODO: optimizations

__all__ = ('ColorStop', 'GradientBase')

from kivy.event import EventDispatcher
from kivy.graphics import Callback, Fbo, Mesh
from kivy.graphics.opengl import glBlendFunc, glBlendFuncSeparate, \
                                    GL_ZERO, GL_ONE_MINUS_SRC_ALPHA, \
                                    GL_SRC_ALPHA, GL_ONE
from kivy.graphics.texture import Texture
from kivy.properties import ColorProperty, BoundedNumericProperty, \
                                ListProperty, ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout


FBO_VERTEX_SHADER = '''
#ifdef GL_ES
    precision highp float;
#endif

attribute float vertexPos;
attribute vec4  vertexColor;

varying vec4 fragmentColor;

void main() {
    fragmentColor = vertexColor;
    gl_Position = vec4(vertexPos * 2.0 - 1.0, 0.0, 0.0, 1.0);
}
'''


FBO_FRAGMENT_SHADER = '''
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 fragmentColor;

void main() {
    gl_FragColor = fragmentColor;
}
'''


class ColorStop(EventDispatcher):
    '''
    The ColorStop class is used together with :class:`LinearGradient` and
    :class:`RadialGradient`. It defines a specific color at a certain position
    within the gradient.
    '''

    color = ColorProperty(allownone=False)
    '''
    The color to display at the stop :attr:`position`.

    :attr:`color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `white`.
    '''

    position = BoundedNumericProperty(
        0.0, min=0.0, max=1.0, errorhandler=lambda x: 1.0 if x > 1.0 else 0.0
    )
    '''
    The position of the color stop. The value should be in the range from 0.0
    (start; one edge of gradient) to 1.0 (end; another edge of gradient).
    If the value exceeds the bounds, it will be set to:

    - 1.0 if the value is greater than 1.0;

    - 0.0 if the value is less than 0.0.

    :attr:`position` is an :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to `0.0`.
    '''

    @property
    def _data(self):
        return self.position, *self.color

    def __repr__(self):
        return f'<ColorStop(position={self.position}, color={self.color})>'


class GradientBase(AnchorLayout):
    '''
    Base class for linear and radial gradients. Do not use it directly; use
    a :class:`~bouquet.gradients.LinearGradient` or
    a :class:`~bouquet.gradients.RadialGradient`.

    .. hint::
        :class:`GradientBase` is an
        :class:`~kivy.uix.anchorlayout.AnchorLayout`
        subclass, so you can put any widget inside it.
    '''

    _1d_gradient_texture = ObjectProperty()

    color_stops = ListProperty()
    '''
    List of :class:`ColorStop` objects, describes how the gradient will look.
    If the list is empty, the gradient will be completely white.

    .. warning::
        bouquet gradients supports up to 1024 color stops.

    :raises ValueError: If the list length is greater than 1024.
    :raises TypeError: If the list contains anything other than
        :class:`ColorStop` objects.

    :attr:`color_stops` is a :class:`~kivy.properties.ListProperty`
    and is empty by default.
    '''

    def __init__(self, **kwargs):
        self.fbind('color_stops', self._on_color_stops)

        self._default_texture = Texture.create(size=(1, 1))
        self._default_texture.blit_buffer(b'\xff\xff\xff\xff')
        self._1d_gradient_texture = self._default_texture

        super(AnchorLayout, self).__init__(**kwargs)

    def _on_color_stops(self, widget, stops):
        if len(stops) > 1024:
            raise ValueError('More than 1024 color stops is not supported.')
        callback = widget._update_mesh
        for s in stops:
            if isinstance(s, ColorStop):
                s.bind(color=callback, position=callback)
            else:
                c = s.__class__.__name__
                raise TypeError(f'Expected ColorStop object, got {c} instead.')
        callback()

    def _update_mesh(self, *args):
        stops = sorted(self.color_stops, key=lambda stop: stop.position)

        if not stops:
            self._1d_gradient_texture = self._default_texture
            return

        first_stop = stops[0]
        if first_stop.position != 0.0:
            stops.insert(0, ColorStop(position=0.0, color=first_stop.color))

        last_stop = stops[-1]
        if last_stop.position != 1.0:
            stops.append(ColorStop(position=1.0, color=last_stop.color))

        mesh = [i for stop in stops for i in stop._data]

        self._1d_gradient_texture = self._render_texture(mesh)

    def _render_texture(self, mesh) -> Texture:
        fbo = Fbo(size=(1024, 1), vs=FBO_VERTEX_SHADER, fs=FBO_FRAGMENT_SHADER)
        with fbo:
            Callback(lambda arg: glBlendFunc(GL_ONE, GL_ZERO))
            Mesh(
                vertices=mesh,
                indices=tuple(range(len(mesh) // 5)),
                mode='line_strip',
                fmt=[(b'vertexPos', 1, 'float'), (b'vertexColor', 4, 'float')]
            )
            Callback(
                lambda arg: glBlendFuncSeparate(
                    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE
                )
            )
        fbo.draw()
        return fbo.texture
