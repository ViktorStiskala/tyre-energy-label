import argparse
import inspect
import json
from typing import Dict, Union

from .label import TyreEnergyLabel


def type_json(value):
    """JSON"""
    return json.loads(value)
type_json.__name__ = 'JSON'


def type_bool(value):
    if value in ["1", "true", "True", "yes"]:
        return True
    if value in ["0", "false", "False", "no"]:
        return False
    raise ValueError("Invalid bool value")
type_bool.__name__ = 'boolean'


class Parser:
    required_args = ('supplier', 'type', 'size', 'tyre_class', 'fuel', 'wet', 'noise', 'level', 'snow', 'ice', 'eprel_id', 'url')

    def __init__(self):
        self.json_keys = inspect.signature(TyreEnergyLabel).parameters.keys()
        self.result = None
        self.parser = self.create_parser()

    def create_parser(self):
        parser = argparse.ArgumentParser(
            epilog='Please specify either a -j/--json or all separate arguments',
            description='''
            Tyre EU energy label generator.\n
            Generates energy label image highlighting performance relating fuel efficiency, safety and noise.
        ''')

        parser.add_argument('-o', '--out', dest='filename', type=argparse.FileType('w', encoding='utf-8'), default='-', help="Output filename (default stdout).")
        parser.add_argument('--no-fonts', action='store_true', help="Do not embed fonts to SVG file")

        json_keys = ', '.join(self.json_keys)
        json_g = parser.add_argument_group('Parse from JSON')
        json_g.add_argument('-j', '--json', type=type_json, help=f'JSON object with the following keys: {json_keys}')

        args_g = parser.add_argument_group("Parse from arguments")
        args_g.add_argument('--supplier', type=str, help="Supplier")
        args_g.add_argument('--type', type=str, help="Type identifier")
        args_g.add_argument('--size', type=str, help="Tyre size (e.g. 185/75 R16)")
        args_g.add_argument('--class', dest='tyre_class', type=str, help="Tyre class (e.g. C2)")
        args_g.add_argument('--fuel', type=str, help="Fuel efficiency grade (A-E)")
        args_g.add_argument('--wet', type=str, help="Wet grip efficiency grade (A-E)")
        args_g.add_argument('--noise', type=int, help="Noise in dB")
        args_g.add_argument('--level', type=str, help="Noise level (A/B/C)")
        args_g.add_argument('--snow', type=type_bool, help="Snow grip icon (yes/no | true/false | 1/0)")
        args_g.add_argument('--ice', type=type_bool, help="Ice grip icon (yes/no | true/false | 1/0)")
        args_g.add_argument('--eprel-id', type=int, help="EPREL ID (e.g. 381667)")
        args_g.add_argument('--url', type=str, help="Link to EPREL database for QR code")

        return parser

    def _validate_json(self, data):
        try:
            diff = set(self.json_keys) - set(data.keys())
            if diff:
                diff_keys = ', '.join(diff)
                self.parser.error(f"Missing following JSON keys: {diff_keys}")
        except AttributeError:
            json_keys = ', '.join(self.json_keys)
            self.parser.error(f"JSON object with the following keys is required: {json_keys}")

    def _validate_params(self, res):
        diff = set(self.required_args) - set(key for key, val in vars(res).items() if val is not None)
        if diff:
            diff_keys = ', '.join(diff)
            self.parser.error(f'Missing arguments: {diff_keys}')

    def get_file(self):
        return self.result.filename

    def parse(self, args=None) -> Dict[str, Union[str, int, bool]]:
        res = self.parser.parse_args(args)
        self.result = res
        if res.json:
            self._validate_json(res.json)
            return res.json
        else:
            self._validate_params(res)

            return {
                'supplier': res.supplier,
                'type_identifier': res.type,
                'size': res.size,
                'tyre_class': res.tyre_class,
                'fuel_efficiency': res.fuel,
                'wet_grip': res.wet,
                'roll_noise': res.noise,
                'noise_level': res.level,
                'snow_grip': res.snow,
                'ice_grip': res.ice,
                'eprel_id': res.eprel_id,
                'eprel_link': res.url,
            }

    def error(self, msg):
        self.parser.error(msg)


def cli():
    parser = Parser()
    data = parser.parse()

    try:
        label = TyreEnergyLabel(**data)
    except ValueError as e:
        parser.error(e)
    else:
        f = parser.get_file()
        svg = label.as_svg(embed_fonts=not parser.result.no_fonts)

        try:
            f.write(svg)
        finally:
            f.close()


