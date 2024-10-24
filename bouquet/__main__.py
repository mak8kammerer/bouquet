import webbrowser

from kivy.lang import Builder
from kivy.app import runTouchApp
from kivy.uix.label import Label
from kivy.properties import StringProperty

from bouquet.gradients import *


DOCS_LINK = 'https://bouquet-kivy.readthedocs.io/en/latest/gradients.html'
LINKS = {
    'linear_gradient':
        DOCS_LINK + '#bouquet.gradients.LinearGradient',
    'linear_gradient_render_texture':
        DOCS_LINK + '#bouquet.gradients.LinearGradient.render_texture',
    'radial_gradient':
        DOCS_LINK + '#bouquet.gradients.RadialGradient',
    'radial_gradient_render_texture':
        DOCS_LINK + '#bouquet.gradients.RadialGradient.render_texture',
    'bilinear_gradient':
        DOCS_LINK + '#bouquet.gradients.BilinearGradient',
    'bilinear_gradient_render_texture':
        DOCS_LINK + '#bouquet.gradients.BilinearGradient.render_texture',
    'conical_gradient':
        DOCS_LINK + '#bouquet.gradients.ConicalGradient',
    'conical_gradient_render_texture':
        DOCS_LINK + '#bouquet.gradients.ConicalGradient.render_texture'
}


class Caption(Label):
    ref = StringProperty()
    label = StringProperty()

    def on_ref_press(self, ref: str):
        link = LINKS.get(ref)
        if link:
            webbrowser.open(link)


KV = '''
#: import window kivy.core.window.Window
#: import ColorStop bouquet.gradients.ColorStop
#: import linear_gradient bouquet.gradients.LinearGradient
#: import radial_gradient bouquet.gradients.RadialGradient
#: import bilinear_gradient bouquet.gradients.BilinearGradient
#: import conical_gradient bouquet.gradients.ConicalGradient

<Caption>:
    size_hint_y: None
    height: self.texture_size[1]
    markup: True
    text: f'[color=#00a8f3][ref={self.ref}]{self.label}[/ref][/color]'

BoxLayout:
    orientation: 'vertical'
    Caption:
        text: '[b]bouquet[/b] library demo'
        font_size: 25
    Caption:
        text: 'Click on the description to open the link in the browser'
        font_size: 15
    ScrollView:
        GridLayout:
            size_hint_y: None
            height: self.minimum_height
            cols: 2
            LinearGradient:
                size_hint_y: None
                height: window.height / 2
                angle: 45
                color_stops: [ \
                    ColorStop(position=0.0, color='red'), \
                    ColorStop(position=1.0, color='yellow'), \
                ]
            Widget:
                size_hint_y: None
                height: window.height / 2
                canvas:
                    Ellipse:
                        pos: self.pos
                        size: self.size
                        texture: linear_gradient.render_texture( \
                            size=self.size, \
                            color_stops=[ \
                                ColorStop(position=0.0, color='red'), \
                                ColorStop(position=1.0, color='yellow'), \
                            ], \
                            angle=45 \
                        )
            Caption:
                ref: 'linear_gradient'
                label: 'LinearGradient widget'
            Caption:
                ref: 'linear_gradient_render_texture'
                label: 'LinearGradient.render_texture() method'
            RadialGradient:
                size_hint_y: None
                height: window.height / 2
                color_stops: [ \
                    ColorStop(position=0.0, color=(1.0, 0.0, 0.0, 1.0)), \
                    ColorStop(position=1.0, color=(1.0, 0.0, 0.0, 0.0)) \
                ]
            Widget:
                canvas:
                    Ellipse:
                        pos: self.pos
                        size: self.size
                        angle_end: 0
                        angle_start: -270
                        texture: radial_gradient.render_texture( \
                            size=self.size, \
                            color_stops=[ \
                                ColorStop( \
                                    position=0.0, color=(1.0, 0.0, 0.0, 1.0) \
                                ), \
                                ColorStop( \
                                    position=1.0, color=(1.0, 0.0, 0.0, 0.0) \
                                ) \
                            ] \
                        )
            Caption:
                ref: 'radial_gradient'
                label: 'RadialGradient widget'
            Caption:
                ref: 'radial_gradient_render_texture'
                label: 'RadialGradient.render_texture() method'
            BilinearGradient:
                size_hint_y: None
                height: window.height / 2
            Widget:
                size_hint_y: None
                height: window.height / 2
                canvas:
                    Triangle:
                        points: [ \
                            self.x, self.y, \
                            self.x + self.width / 2, self.y + self.height, \
                            self.x + self.width, self.y \
                        ]
                        tex_coords: [1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0]
                        texture: bilinear_gradient.render_texture( \
                            size=self.size \
                        )
            Caption:
                ref: 'bilinear_gradient'
                label: 'BilinearGradient widget'
            Caption:
                ref: 'bilinear_gradient_render_texture'
                label: 'BilinearGradient.render_texture() method'
            ConicalGradient:
                size_hint_y: None
                height: window.height / 2
                color_stops: [ \
                    ColorStop(position=0.0, color='cyan'), \
                    ColorStop(position=0.3, color='magenta'), \
                    ColorStop(position=0.6, color='yellow'), \
                    ColorStop(position=1.0, color='cyan')  \
                ]
            Widget:
                canvas:
                    Ellipse:
                        pos: self.pos
                        size: self.size
                        texture: conical_gradient.render_texture( \
                            size=self.size, \
                            color_stops=[ \
                                ColorStop(position=0.0, color='cyan'), \
                                ColorStop(position=0.3, color='magenta'), \
                                ColorStop(position=0.6, color='yellow'), \
                                ColorStop(position=1.0, color='cyan')  \
                            ] \
                        )
            Caption:
                ref: 'conical_gradient'
                label: 'ConicalGradient widget'
            Caption:
                ref: 'conical_gradient_render_texture'
                label: 'ConicalGradient.render_texture() method'
'''


runTouchApp(Builder.load_string(KV))
