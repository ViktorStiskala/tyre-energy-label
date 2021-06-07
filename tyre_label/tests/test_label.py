import copy
import os
import tempfile
from unittest import TestCase
import xml.etree.ElementTree as ET

from tyre_label import TyreEnergyLabel

TEST_LABEL_DATA = {
    'supplier': 'Cool Tyre',
    'type_identifier': '94385300',
    'size': '185/75 R16',
    'tyre_class': 'C2',
    'fuel_efficiency': 'E',
    'wet_grip': 'A',
    'roll_noise': 72,
    'noise_level': 'C',
    'snow_grip': True,
    'ice_grip': True,
    'eprel_id': 381667,
    'eprel_link': 'https://eprel.ec.europa.eu/qr/381667'
}


class TestLabel(TestCase):
    def assertQr(self, svg):
        root = ET.fromstring(svg)
        namespaces = {'svg': 'http://www.w3.org/2000/svg'}

        svg_g = root.find('.//svg:g[@id="QR"]', namespaces=namespaces)
        qr_path = svg_g.find('.//svg:path', namespaces=namespaces)

        self.assertRegex(qr_path.attrib['d'], r'.*M\s[\d\.]+.*', msg='SVG file should contain QR code')

    def test_svg_output(self):
        label = TyreEnergyLabel(**TEST_LABEL_DATA)

        svg_data = label.as_svg()

        self.assertIn('<svg xmlns', svg_data)

    def test_file_output(self):
        label = TyreEnergyLabel(**TEST_LABEL_DATA)

        with tempfile.TemporaryDirectory() as path:
            test_file = os.path.join(path, 'test.svg')
            label.save(test_file)

            with open(test_file, 'r') as f:
                content = f.read()
                self.assertIn('<svg xmlns', content)

    def test_fonts(self):
        label = TyreEnergyLabel(**TEST_LABEL_DATA)

        no_fonts = label.as_svg(embed_fonts=False)
        include_fonts = label.as_svg(embed_fonts=True)

        self.assertNotIn('@font-face', no_fonts)
        self.assertIn('@font-face', include_fonts)

    def test_content(self):
        label = TyreEnergyLabel(**TEST_LABEL_DATA)

        self.assertQr(label.as_svg())

    def test_qrcode_without_link(self):
        test_data = copy.deepcopy(TEST_LABEL_DATA)
        test_data.pop('eprel_link')

        label = TyreEnergyLabel(**test_data)
        self.assertQr(label.as_svg())


