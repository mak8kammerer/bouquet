# TODO: test transparency

from kivy.tests.common import GraphicUnitTest


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
        

    def test_gradient_base(self):
        from bouquet.gradients import ColorStop
        from bouquet.gradients.base import GradientBase

        render = self.render

        wid = GradientBase()
        render(wid)
        
        default_texture = wid._default_texture
        pixels = default_texture.pixels
        
        texture = wid._1d_gradient_texture
        self.assertEqual(texture, default_texture)

        self.assertEqual(default_texture.width, 1)
        self.assertEqual(default_texture.height, 1)

        self.assertEqual(len(pixels), 4)
        self.assertEqual(pixels, b'\xff\xff\xff\xff')

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
        self.assertEqual(pixels[4 * 512: 4 * 513], b'\x80\x80\x80\xff')
        # 1.0 -> left -> white
        self.assertEqual(pixels[-4:], b'\xff\xff\xff\xff')

        wid.color_stops = [
            ColorStop(position=0.75, color=[1.0, 0.0, 0.0, 0.0]),
            ColorStop(position=0.25, color=[0.0, 0.0, 1.0, 1.0])
        ]
        texture = wid._1d_gradient_texture
        pixels = texture.pixels

        self.assertEqual(texture.height, 1)
        self.assertEqual(texture.width, 1024)

        self.assertEqual(len(pixels), 4 * 1024)
        # 0.0 -> opaque blue
        self.assertEqual(pixels[:4], b'\x00\x00\xff\xff')
        # 0.25 -> opaque blue
        self.assertEqual(pixels[4 * 256: 4 * 257], b'\x00\x00\xff\xff')
        # 0.75 -> transparent red == transparent black
        self.assertEqual(pixels[4 * 768: 4 * 769], b'\x00\x00\x00\x00')
        # 1.0 -> transparent red == transparent black
        self.assertEqual(pixels[-4:], b'\x00\x00\x00\x00')

        with self.assertRaises(ValueError):
            wid.color_stops = [ColorStop() for _ in range(1025)]

        with self.assertRaises(TypeError):
            wid.color_stops = [1]

    def test_linear_gradient(self):
        from bouquet.gradients import ColorStop, LinearGradient

        render = self.render

        wid = LinearGradient()
        render(wid)

        wid.color_stops = [ColorStop(color='red')]
        render(wid)

        wid.color_stops.append(ColorStop(color='#ffff00ff', position=0.75))
        wid.angle = -70
        render(wid)

        texture = LinearGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))
        self.assertEqual(len(texture.pixels), 4 * 100 * 100)
        self.assertEqual(texture.pixels, b'\xff\xff\xff\xff' * 100 * 100)

        texture = LinearGradient.render_texture(
            color_stops=[ColorStop(color='red')], size=(50, 70)
        )
        self.assertEqual(texture.size, (50, 70))
        self.assertEqual(len(texture.pixels), 4 * 50 * 70)
        self.assertEqual(texture.pixels, b'\xff\x00\x00\xff' * 70 * 50)

        # horizontal
        texture = LinearGradient.render_texture(
            color_stops=[
                ColorStop(color='red'),
                ColorStop(color=(0.0, 0.0, 0.0, 1.0), position=1.0)
            ],
            size=(1, 3)
        )
        self.assertEqual(texture.size, (1, 3))
        self.assertEqual(len(texture.pixels), 4 * 1 * 3)
        color = b'\x80\x00\x00\xff'  # (128, 0, 0, 255)
        self.assertEqual(texture.pixels[4:8], color)

        # vertical
        texture = LinearGradient.render_texture(
            color_stops=[
                ColorStop(color='#ffffff'),
                ColorStop(color='#ff00ffff', position=1.0)
            ],
            size=(3, 1)
        )
        self.assertEqual(texture.size, (3, 1))
        self.assertEqual(len(texture.pixels), 4 * 3 * 1)
        color = b'\xff\x80\xff\xff'  # (255, 128, 255, 255)
        self.assertEqual(texture.pixels[4:8], color)

    def test_bilinear_gradient(self):
        from bouquet.gradients import BilinearGradient

        render = self.render

        wid = BilinearGradient()
        render(wid)

        wid.bottom_left_color = '#ff0000'
        render(wid)

        texture = BilinearGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))

        tex_size = (500, 600)
        texture = BilinearGradient.render_texture(
            size=tex_size,
            bottom_left_color='#00000000'
        )
        self.assertEqual(texture.size, tex_size)

        pixels = texture.pixels
        self.assertEqual(len(pixels), tex_size[0] * tex_size[1] * 4)

        # bottom left corner -> transparent black
        self.assertEqual(pixels[:4], b'\x00\x00\x00\x00')
        # top right corner -> yellow
        self.assertEqual(pixels[-4:], b'\xff\xff\x00\xff')

    def test_radial_gradient(self):
        from kivy.graphics.fbo import Fbo
        from bouquet.gradients import RadialGradient

        render = self.render

        wid = RadialGradient()
        render(wid)

        wid.border_color = '#ff0000'
        render(wid)

        texture = RadialGradient.render_texture()
        self.assertEqual(texture.size, (100, 100))

        tex_size = (500, 500)
        texture = RadialGradient.render_texture(
            size=tex_size,
            border_color='#00000000'
        )
        self.assertEqual(texture.size, tex_size)

        pixels = texture.pixels
        self.assertEqual(len(pixels), tex_size[0] * tex_size[1] * 4)

        # bottom left corner -> transparent black
        self.assertEqual(pixels[:4], b'\x00\x00\x00\x00')
        # TODO: test center_color here
