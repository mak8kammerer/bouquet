# TODO: reorganize

from kivy.lang import Builder
from kivy.app import runTouchApp

from bouquet.gradients import *

KV = '''
#: import window kivy.core.window.Window
#: import ColorStop bouquet.gradients.ColorStop
#: import linear_gradient bouquet.gradients.LinearGradient
#: import radial_gradient bouquet.gradients.RadialGradient
#: import bilinear_gradient bouquet.gradients.BilinearGradient

#: import open_link webbrowser.open
#: set ref_start '[color=#00a8f3][ref=ref]'
#: set ref_end '[/ref][/color]'
#: set gradient_docs \
        'https://bouquet-kivy.readthedocs.io/en/latest/gradients.html'
#: set linear_gradient_link \
        gradient_docs + '#bouquet.gradients.LinearGradient'
#: set linear_gradient_render_texture_link \
        gradient_docs + '#bouquet.gradients.LinearGradient.render_texture'
#: set radial_gradient_link \
        gradient_docs + '#bouquet.gradients.RadialGradient'
#: set radial_gradient_render_texture_link \
        gradient_docs + '#bouquet.gradients.RadialGradient.render_texture'
#: set bilinear_gradient_link \
        gradient_docs + '#bouquet.gradients.BilinearGradient'
#: set bilinear_gradient_render_texture_link \
        gradient_docs + '#bouquet.gradients.BilinearGradient.render_texture'

<Caption@Label>:
    markup: True
    size_hint_y: None
    height: self.texture_size[1]

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
                text: ref_start + 'LinearGradient widget' + ref_end
                on_ref_press: open_link(linear_gradient_link)
            Caption:
                text: ref_start + 'LinearGradient.render_texture() method' \
                                                                    + ref_end
                on_ref_press: open_link(linear_gradient_render_texture_link)
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
                text: ref_start + 'RadialGradient widget' + ref_end
                on_ref_press: open_link(radial_gradient_link)
            Caption:
                text: ref_start + 'RadialGradient.render_texture() method' \
                                                                    + ref_end
                on_ref_press: open_link(radial_gradient_render_texture_link)
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
                text: ref_start + 'BilinearGradient widget' + ref_end
                on_ref_press: open_link(bilinear_gradient_link)
            Caption:
                text: ref_start + 'BilinearGradient.render_texture() method' \
                                                                    + ref_end
                on_ref_press: open_link(bilinear_gradient_render_texture_link)
'''


runTouchApp(Builder.load_string(KV))
