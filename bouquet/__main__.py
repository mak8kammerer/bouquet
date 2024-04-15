# TODO: reorganize

from kivy.lang import Builder
from kivy.app import runTouchApp

from bouquet.gradients import *

KV = '''
#: import window kivy.core.window.Window
#: import linear_gradient bouquet.gradients.LinearGradient
#: import radial_gradient bouquet.gradients.RadialGradient

<Caption@Label>:
    size_hint_y: None
    height: self.texture_size[1]

BoxLayout:
    orientation: 'vertical'
    Caption:
        markup: True
        text: '[b]bouquet[/b] library demo'
        font_size: 25
    ScrollView:
        BoxLayout:
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            LinearGradient:
                size_hint_y: None
                height: window.height / 2
            Caption:
                text: 'LinearGradient widget'
            RadialGradient:
                size_hint_y: None
                height: window.height / 2
            Caption:
                text: 'RadialGradient widget'
            Widget:
                size_hint_y: None
                height: window.height / 2
                canvas:
                    Ellipse:
                        pos: self.pos
                        size: self.size
                        texture: linear_gradient.render_texture(size=self.size)
            Caption:
                text: 'Ellipse with LinearGradient texture'
            Widget:
                size_hint_y: None
                height: window.height / 2
                canvas:
                    Mesh:
                        mode: 'triangles'
                        indices: [0, 1, 2]
                        vertices: [ \
                            self.x, self.y, 0.0, 0.0, \
                            self.x + self.width, self.y, 1.0, 0.0, \
                            self.x + self.width / 2, self.y + self.height, \
                            0.5, 1.0 \
                        ]
                        texture: radial_gradient.render_texture(size=self.size)
            Caption:
                text: 'Triangle with RadialGradient texture'
'''


runTouchApp(Builder.load_string(KV))
