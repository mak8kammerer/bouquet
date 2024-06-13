from kivy.tests.common import GraphicUnitTest


class GradientsTests(GraphicUnitTest):

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
