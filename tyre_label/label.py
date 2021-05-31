from pathlib import Path

import qrcode
from qrcode.image.svg import SvgPathImage
import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader

ROOT_DIR = Path(__file__).resolve().parent


class TyreEnergyLabel:
    """
    Tyre energy label generator.

    Example usage:

    label = TyreEnergyLabel(
        supplier='Cool Tyre',
        type_identifier='94385300',
        size='185/75 R16',
        tyre_class='C2',
        fuel_efficiency='E',
        wet_grip='A',
        roll_noise=72,
        noise_level='C',
        snow_grip=True,
        ice_grip=True,
        eprel_id=381667,
        eprel_link='https://eprel.ec.europa.eu/qr/381667'
    )
    label.save('example.svg')

    # optional: get SVG as a string
    svg_data = label.as_svg(embed_fonts=True, include_link=True)
    """

    META = {
        'rating_y': {'A': 38, 'B': 60, 'C': 83, 'D': 106, 'E': 128},
        'icon_x': {
            1: [73],
            2: [48, 124],
            3: [11, 87, 144]
        },
        'allowed_ranges': ('A', 'B', 'C', 'D', 'E')
    }

    def __init__(self, supplier: str, type_identifier: str, size: str, tyre_class: str,
                 fuel_efficiency: str, wet_grip: str, roll_noise: int, noise_level: str,
                 snow_grip: bool, ice_grip: bool, eprel_id: int, eprel_link: str):

        self.data = {
            'supplier': supplier,
            'type_identifier': type_identifier,
            'size': size,
            'class': tyre_class,
            'fuel_efficiency': fuel_efficiency.upper(),
            'wet_grip': wet_grip.upper(),
            'roll_noise': roll_noise,
            'noise_level': noise_level.upper(),
            'snow_grip': snow_grip,
            'ice_grip': ice_grip,
            'eprel_id': eprel_id,
            'eprel_link': eprel_link,
            'icon_count': sum([snow_grip, ice_grip]) + 1
        }
        if noise_level.upper() not in ('A', 'B', 'C'):
            raise ValueError(f'Invalid noise level "{noise_level}", expected A, B or C')

        self.jinja_env = Environment(loader=FileSystemLoader(ROOT_DIR / 'templates'))

    def get_qrcode(self) -> str:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=11,
            border=0
        )
        qr.add_data(self.data['eprel_link'])
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white", image_factory=SvgPathImage)
        svg_path = img.make_path()

        return ET.tostring(svg_path, encoding='unicode')

    def as_svg(self, embed_fonts: bool = True, include_link: bool = True) -> str:
        template = self.jinja_env.get_template('label.svg.j2')

        svg = template.render(
            embed_fonts=embed_fonts,
            include_link=include_link,
            tyre=self.data,
            meta=self.META,
            qr_code=self.get_qrcode()
        )

        return svg

    def save(self, filename):
        with open(filename, 'w') as file:
            file.write(self.as_svg())
