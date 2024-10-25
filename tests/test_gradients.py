import os

import pytest

from kivy.tests.common import GraphicUnitTest


is_github_actions = pytest.mark.skipif(
    os.getenv('GITHUB_ACTIONS', default='false') == 'true',
    reason='Skip texture tests on GitHub Actions'
    # When running tests that interact with the Texture class on
    # GitHub Actions, strange error occur. Example snippet:
    #   from kivy.graphics.texture import Texture
    #   texture = Texture.create(size=(1, 1))
    #   texture.blit_buffer(b'\xff\xff\xff\xff')
    #   self.assertEqual(texture.pixels, b'\xff\xff\xff\xff')
    # Result:
    #   AssertionError: b'\x00\x00\x00\x00' != b'\xff\xff\xff\xff'
    # Therefore, we skip texture testing on GitHub Actions.
)


class GradientsTests(GraphicUnitTest):

    def test_color_stop(self):
        from bouquet.gradients import ColorStop

        c = ColorStop()
        self.assertEqual(c.position, 0.0)
        self.assertEqual(c.color, [1.0, 1.0, 1.0, 1.0])

        c.position = 1.5
        self.assertEqual(c.position, 1.0)

        c.position = -1.0
        self.assertEqual(c.position, 0.0)

        c = ColorStop(position=0.5, color='red')
        self.assertEqual(c.position, 0.5)
        self.assertEqual(c.color, [1.0, 0.0, 0.0, 1.0])

        with self.assertRaises(ValueError):
            c.color = None

        self.assertEqual(c._data, (0.5, 1.0, 0.0, 0.0, 1.0))

        repr_msg = '<ColorStop(position=0.5, color=[1.0, 0.0, 0.0, 1.0])>'
        self.assertEqual(repr(c), repr_msg)

    def test_gradient_base_widget(self):
        from bouquet.gradients import ColorStop
        from bouquet.gradients.base import GradientBase

        wid = GradientBase()
        self.render(wid)

        with self.assertRaises(ValueError):
            wid.color_stops = [ColorStop() for _ in range(1025)]

        with self.assertRaises(TypeError):
            wid.color_stops = [1]

    @is_github_actions
    def test_gradient_base_texture(self):
        from bouquet.gradients import ColorStop
        from bouquet.gradients.base import GradientBase

        wid = GradientBase()
        default_texture = wid._default_texture
        pixels = default_texture.pixels
        texture = wid._1d_gradient_texture
        self.assertEqual(texture, default_texture)
        self.assertEqual(default_texture.width, 1)
        self.assertEqual(default_texture.height, 1)
        self.assertEqual(len(pixels), 4)
        self.assertEqual(pixels, b'\xff\xff\xff\xff')

        wid.color_stops = [
            ColorStop(color=(0.0, 1.0, 0.5, 0.25))
        ]
        texture = wid._1d_gradient_texture
        pixels = texture.pixels
        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 1024)
        self.assertEqual(len(pixels), 4 * 1024)
        self.assertEqual(pixels, b'\x00\xff\x80@' * 1024)   # (0, 255, 128, 64)

        wid.color_stops = [
            ColorStop(position=0.0, color='black'),
            ColorStop(position=1.0, color='white')
        ]
        texture = wid._1d_gradient_texture
        pixels = texture.pixels
        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 1024)
        self.assertEqual(len(pixels), 4 * 1024)
        # 0.0 -> right -> black
        self.assertEqual(pixels[:4], b'\x00\x00\x00\xff')
        # 0.5 -> middle -> gray
        self.assertEqual(pixels[4 * 512:4 * 513], b'\x80\x80\x80\xff')
        # 1.0 -> left -> white
        self.assertEqual(pixels[-4:], b'\xff\xff\xff\xff')

        # alpha blending test
        wid.color_stops = [
            ColorStop(position=0.75, color=[1.0, 0.0, 0.0, 0.0]),
            ColorStop(position=0.25, color=[0.0, 0.0, 1.0, 1.0])
        ]
        texture = wid._1d_gradient_texture
        pixels = texture.pixels
        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 1024)
        self.assertEqual(len(pixels), 4 * 1024)
        # 0.0 -> opaque blue -> (0, 0, 255, 255)
        self.assertEqual(pixels[:4], b'\x00\x00\xff\xff')
        # 0.25 -> opaque blue -> (0, 0, 255, 255)
        self.assertEqual(pixels[4 * 256:4 * 257], b'\x00\x00\xff\xff')
        # 0.75 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(pixels[4 * 768:4 * 769], b'\xff\x00\x00\x00')
        # 1.0 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(pixels[-4:], b'\xff\x00\x00\x00')

    def test_linear_gradient_widget(self):
        from bouquet.gradients import ColorStop, LinearGradient

        render = self.render

        wid = LinearGradient()
        render(wid)

        wid.color_stops = [ColorStop(color='red')]
        render(wid)

        wid.color_stops.append(ColorStop(color='#ffff00ff', position=0.75))
        wid.angle = -70
        render(wid)

    @is_github_actions
    def test_linear_gradient_texture(self):
        from bouquet.gradients import ColorStop, LinearGradient

        texture = LinearGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))
        self.assertEqual(len(texture.pixels), 4 * 100 * 100)
        self.assertEqual(texture.pixels, b'\xff\xff\xff\xff' * 100 * 100)

        texture = LinearGradient.render_texture(width=64)
        self.assertEqual(texture.size, (64, 100))

        texture = LinearGradient.render_texture(height=128)
        self.assertEqual(texture.size, (100, 128))

        texture = LinearGradient.render_texture(
            color_stops=[ColorStop(color='red')],
            width=256, height=128
        )
        self.assertEqual(texture.size, (256, 128))
        self.assertEqual(len(texture.pixels), 4 * 256 * 128)
        self.assertEqual(texture.pixels, b'\xff\x00\x00\xff' * 256 * 128)

        # rotation test
        color_stops = [
            ColorStop(position=0.3, color='red'),
            ColorStop(position=0.6, color='blue'),
            ColorStop(position=1.0, color='white')
        ]
        horizontal = LinearGradient.render_texture(
            color_stops=color_stops, width=1, height=1000
        )
        vertical = LinearGradient.render_texture(
            color_stops=color_stops, size=(1000, 1), angle=90
        )
        self.assertEqual(horizontal.size, (1, 1000))
        self.assertEqual(vertical.width, 1000)
        self.assertEqual(vertical.height, 1)
        self.assertEqual(len(horizontal.pixels), len(vertical.pixels))
        self.assertEqual(horizontal.pixels, vertical.pixels)

        # test blending (horizontal)
        texture = LinearGradient.render_texture(
            color_stops=[
                ColorStop(color='red'),
                ColorStop(color=(0.0, 0.0, 0.0, 1.0), position=1.0)
            ],
            size=(1, 3)
        )
        self.assertEqual(texture.size, (1, 3))
        self.assertEqual(len(texture.pixels), 4 * 1 * 3)
        # 0.5 -> marron -> (128, 0, 0, 255)
        self.assertEqual(texture.pixels[4:8], b'\x80\x00\x00\xff')

        # test blending (vertical)
        texture = LinearGradient.render_texture(
            color_stops=[
                ColorStop(color='#ffffff'),
                ColorStop(color='#ff00ffff', position=1.0)
            ],
            size=(3, 1)
        )
        self.assertEqual(texture.size, (3, 1))
        self.assertEqual(len(texture.pixels), 4 * 3 * 1)
        # 0.5 -> light fuchsia -> (255, 128, 255, 255)
        self.assertEqual(texture.pixels[4:8], b'\xff\x80\xff\xff')

        # alpha blending test
        texture = LinearGradient.render_texture(
            color_stops=[
                ColorStop(position=0.75, color=[1.0, 0.0, 0.0, 0.0]),
                ColorStop(position=0.25, color=[0.0, 0.0, 1.0, 1.0])
            ],
            width=1000, height=1, angle=90
        )
        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 1000)
        self.assertEqual(len(texture.pixels), 4 * 1000 * 1)
        # 0.0 -> opaque blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[:4], b'\x00\x00\xff\xff')
        # 0.25 -> opaque blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[4 * 249:4 * 250], b'\x00\x00\xff\xff')
        # 0.75 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(texture.pixels[4 * 749:4 * 750], b'\xff\x00\x00\x00')
        # # 1.0 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(texture.pixels[-4:], b'\xff\x00\x00\x00')

    def test_bilinear_gradient(self):
        from bouquet.gradients import BilinearGradient

        render = self.render

        wid = BilinearGradient()
        render(wid)

        wid.bottom_left_color = '#ff0000'
        render(wid)

        wid.bottom_right_color = '#ff00ff'
        wid.top_left_color = '#ffff00'
        wid.top_right_color = '#ffffff'
        render(wid)

        texture = BilinearGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))

        texture = BilinearGradient.render_texture(width=128)
        self.assertEqual(texture.size, (128, 100))

        texture = BilinearGradient.render_texture(height=256)
        self.assertEqual(texture.size, (100, 256))

        texture = BilinearGradient.render_texture(
            width=400, height=600,
            bottom_left_color='#ff0000',
            bottom_right_color='#ff0000ff',
            top_left_color=[1.0, 0.0, 0.0],
            top_right_color=(1.0, 0.0, 0.0, 1.0)
        )
        self.assertEqual(texture.width, 400)
        self.assertEqual(texture.height, 600)
        self.assertEqual(len(texture.pixels), 4 * 400 * 600)
        self.assertEqual(texture.pixels, b'\xff\x00\x00\xff' * 400 * 600)

        # alpha blending test
        texture = BilinearGradient.render_texture(
            bottom_left_color='red',
            bottom_right_color='red',
            top_left_color='#0000ff00',
            top_right_color='#0000ff00',
            width=1000, height=1000
        )
        self.assertEqual(texture.size, (1000, 1000))
        self.assertEqual(len(texture.pixels), 4 * 1000 * 1000)
        # top -> opaque red -> (255, 0, 0, 255)
        self.assertEqual(texture.pixels[:1000 * 4], b'\xff\x00\x00\xff' * 1000)
        # bottom -> transparent blue -> (0, 0, 255, 0)
        self.assertEqual(texture.pixels[-1000 * 4:], b'\x00\x00\xff\x00' * 1000)

    def test_radial_gradient_widget(self):
        from bouquet.gradients import ColorStop, RadialGradient

        render = self.render

        wid = RadialGradient()
        render(wid)

        wid.color_stops = [ColorStop(color='purple')]
        render(wid)

        wid.color_stops = [ColorStop(position=0.66)]
        render(wid)

        wid.color_stops[0].position = 0.25
        wid.color_stops[0].color = (1.0, 0.0, 0.25, 0.8)
        render(wid)

        wid.color_stops = [
            ColorStop(position=0.0, color='pink'),
            ColorStop(position=1.0, color='blue')
        ]
        render(wid)

        wid.color_stops = [
            ColorStop(position=0.3, color=(1.0, 0.0, 0.5, 1.0)),
            ColorStop(position=0.8, color=(0.8, 1.0, 0.3, 0.9))
        ]
        render(wid)

        wid.color_stops = [
            ColorStop(position=0.0, color='orange'),
            ColorStop(position=0.5, color='yellow'),
            ColorStop(position=1.0, color='red')
        ]
        render(wid)

        wid.gradient_center_x = 0.35
        render(wid)

        wid.gradient_center_y = 0.14
        render(wid)

        wid.gradient_center_position = (0.0, 0.0)
        render(wid)

        wid.radius = 2.5
        render(wid)

        wid.radius = 0.0
        render(wid)

        wid.radius = -1.0
        render(wid)

    @is_github_actions
    def test_radial_gradient_texture(self):
        from bouquet.gradients import ColorStop, RadialGradient

        texture = RadialGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))

        texture = RadialGradient.render_texture(width=32)
        self.assertEqual(texture.size, (32, 100))

        texture = RadialGradient.render_texture(height=512)
        self.assertEqual(texture.size, (100, 512))

        texture = RadialGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))
        self.assertEqual(len(texture.pixels), 4 * 100 * 100)
        self.assertEqual(texture.pixels, b'\xff\xff\xff\xff' * 100 * 100)

        texture = RadialGradient.render_texture(
            color_stops=[ColorStop(position=0.5, color='yellow')],
            width=256, height=128
        )
        self.assertEqual(texture.size, (256, 128))
        self.assertEqual(len(texture.pixels), 4 * 256 * 128)
        self.assertEqual(texture.pixels, b'\xff\xff\x00\xff' * 256 * 128)

        texture = RadialGradient.render_texture(
            color_stops=[
                ColorStop(position=0.0, color='red'),
                ColorStop(position=1.0, color='white')
            ],
            size=(512, 256), radius=0.0
        )
        self.assertEqual(texture.size, (512, 256))
        self.assertEqual(len(texture.pixels), 4 * 512 * 256)
        self.assertEqual(texture.pixels, b'\xff\xff\xff\xff' * 512 * 256)

        texture = RadialGradient.render_texture(
            color_stops=[
                ColorStop(position=0.0, color='red'),
                ColorStop(position=0.5, color='yellow'),
                ColorStop(position=1.0, color='white')
            ],
            height=1, width=2000
        )
        self.assertEqual(texture.size, (2000, 1))
        self.assertEqual(len(texture.pixels), 4 * 2000 * 1)
        # 0.0 -> white -> (255, 255, 255, 255)
        self.assertEqual(texture.pixels[:4], b'\xff\xff\xff\xff')
        # 0.5 -> yellow -> (255, 255, 0, 255)
        self.assertEqual(texture.pixels[499 * 4:500 * 4], b'\xff\xff\x00\xff')
        # 1.0 -> red -> (255, 0, 0, 255)
        self.assertEqual(texture.pixels[999 * 4:1000 * 4], b'\xff\x00\x00\xff')
        # 0.5 -> yellow -> (255, 255, 0, 255)
        self.assertEqual(texture.pixels[1499 * 4:1500 * 4], b'\xff\xff\x00\xff')
        # 0.0 -> white -> (255, 255, 255, 255)
        self.assertEqual(texture.pixels[-4:], b'\xff\xff\xff\xff')

        texture = RadialGradient.render_texture(
            color_stops=[
                ColorStop(position=0.0, color=[1.0, 0.0, 0.0]),
                ColorStop(position=0.5, color=[0.0, 1.0, 0.0]),
                ColorStop(position=1.0, color=[0.0, 0.0, 1.0])
            ],
            height=1, width=2000, gradient_center_x=0.0
        )
        self.assertEqual(texture.size, (2000, 1))
        self.assertEqual(len(texture.pixels), 4 * 2000 * 1)
        # 0.0 -> red -> (255, 0, 0, 255)
        self.assertEqual(texture.pixels[:4], b'\xff\x00\x00\xff')
        # 0.25 -> green -> (0, 255, 0, 255)
        self.assertEqual(texture.pixels[499 * 4:500 * 4], b'\x00\xff\x00\xff')
        # 0.5 - 1.0 -> blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[4 * 1000:], b'\x00\x00\xff\xff' * 1000)

        texture = RadialGradient.render_texture(
            color_stops=[
                ColorStop(position=0.0, color=[1.0, 0.0, 0.0]),
                ColorStop(position=0.5, color=[0.0, 1.0, 0.0]),
                ColorStop(position=1.0, color=[0.0, 0.0, 1.0])
            ],
            size=(1, 2000), gradient_center_y=0.0
        )
        self.assertEqual(texture.size, (1, 2000))
        self.assertEqual(len(texture.pixels), 4 * 1 * 2000)
        # 1.0 - 0.5 -> blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[:4 * 1000], b'\x00\x00\xff\xff' * 1000)
        # 0.25 -> green -> (0, 255, 0, 255)
        self.assertEqual(texture.pixels[1499 * 4:1500 * 4], b'\x00\xff\x00\xff')
        # 0.0 -> red -> (255, 0, 0, 255)
        self.assertEqual(texture.pixels[-4:], b'\xff\x00\x00\xff')

        texture = RadialGradient.render_texture(
            color_stops=[
                ColorStop(position=0.0, color=[1.0, 0.0, 0.0]),
                ColorStop(position=0.5, color=[0.0, 1.0, 0.0]),
                ColorStop(position=1.0, color=[0.0, 0.0, 1.0])
            ],
            size=(2000, 1), radius=2.0,
            gradient_center_position=(0.0, 0.5)
        )
        self.assertEqual(texture.size, (2000, 1))
        self.assertEqual(len(texture.pixels), 4 * 2000 * 1)
        # 0.0 -> red -> (255, 0, 0, 255)
        self.assertEqual(texture.pixels[:4], b'\xff\x00\x00\xff')
        # 0.5 -> green -> (0, 255, 0, 255)
        self.assertEqual(texture.pixels[999 * 4:1000 * 4], b'\x00\xff\x00\xff')
        # 1.0 -> blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[-4:], b'\x00\x00\xff\xff')

        # alpha blending test
        texture = RadialGradient.render_texture(
            color_stops=[
                ColorStop(position=0.75, color=[1.0, 0.0, 0.0, 0.0]),
                ColorStop(position=0.25, color=[0.0, 0.0, 1.0, 1.0])
            ],
            width=2000, height=1
        )
        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 2000)
        self.assertEqual(len(texture.pixels), 4 * 2000 * 1)
        # 0.0 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(texture.pixels[:4], b'\xff\x00\x00\x00')
        # 0.25 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(texture.pixels[4 * 249:4 * 250], b'\xff\x00\x00\x00')
        # 0.75 -> opaque blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[4 * 749:4 * 750], b'\x00\x00\xff\xff')
        # 1.0 -> opaque blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[4 * 999:4 * 1000], b'\x00\x00\xff\xff')
        # 0.75 -> opaque blue -> (0, 0, 255, 255)
        self.assertEqual(texture.pixels[4 * 1249:4 * 1250], b'\x00\x00\xff\xff')
        # 0.25 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(texture.pixels[4 * 1749:4 * 1750], b'\xff\x00\x00\x00')
        # 0.0 -> transparent red -> (255, 0, 0, 0)
        self.assertEqual(texture.pixels[-4:], b'\xff\x00\x00\x00')

    def test_conical_gradient_widget(self):
        from bouquet.gradients import ColorStop, ConicalGradient

        render = self.render

        wid = ConicalGradient()
        render(wid)

        wid.color_stops = [ColorStop(color='cyan')]
        render(wid)

        wid.color_stops.append(ColorStop(color='#ffffff', position=0.2))
        render(wid)
        
        wid.gradient_center_x = 0.0
        render(wid)
        
        wid.gradient_center_y = 0.1
        render(wid)
        
        wid.gradient_center_pos = (0.5, 0.5)
        render(wid)

    def test_conical_gradient_widget(self):
        from bouquet.gradients import ColorStop, ConicalGradient
        
        texture = ConicalGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))

        texture = ConicalGradient.render_texture(width=128)
        self.assertEqual(texture.size, (128, 100))

        texture = ConicalGradient.render_texture(height=256)
        self.assertEqual(texture.size, (100, 256))

        texture = ConicalGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))
        self.assertEqual(len(texture.pixels), 4 * 100 * 100)
        self.assertEqual(texture.pixels, b'\xff\xff\xff\xff' * 100 * 100)

        texture = ConicalGradient.render_texture(
            color_stops=[
                ColorStop(color=(1.0, 1.0, 0.0, 0.0))
            ], size=(50, 50)
        )
        self.assertEqual(texture.size, (50, 50))
        self.assertEqual(len(texture.pixels), 4 * 50 * 50)
        self.assertEqual(texture.pixels, b'\xff\xff\x00\x00' * 50 * 50)


        texture = ConicalGradient.render_texture(
            color_stops=[
                ColorStop(position=0.0, color=(1.0, 0.0, 0.0)),
                ColorStop(position=1.0, color=(1.0, 1.0, 0.0))
            ], width=1000, height=1
        )
        self.assertEqual(texture.size, (1000, 1))
        self.assertEqual(len(texture.pixels), 4 * 1000 * 1)
        self.assertEqual(texture.pixels[:4 ], b'\xff\x80\x00\xff')
        self.assertEqual(texture.pixels[-4:], b'\xff\xff\x00\xff')
