# Python tyres EU energy label generator
[![PyPI version](https://badge.fury.io/py/tyre-energy-label.svg)](https://badge.fury.io/py/tyre-energy-label)

Python library for [EU tyre energy labels][1]. Creates a label according to the specification as an SVG file.

[![Example label](https://raw.githubusercontent.com/ViktorStiskala/tyre-energy-label/main/example/example.png)](https://raw.githubusercontent.com/ViktorStiskala/tyre-energy-label/main/example/example.svg)

## Installation

```shell
$ pip install tyre-energy-label
```

## Usage

```python
from tyre_label import TyreEnergyLabel

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
```

If you don't specify `eprel_link`, it will be automatically generated from `eprel_id`.

## Command line interface
The package installs `tyre-label` CLI. Use `$ tyre-label --help` for the list of available options.

### Example usage

```shell
$ tyre-label \
    --supplier "Cool Tyre" \
    --type "94385300" \
    --size "185/75 R16" \
    --class "C2" \
    --fuel C \
    --wet A \
    --noise 72 \
    --level A \
    --snow 1 \
    --ice 1 \
    --eprel-id 381667 \
    --url "https://eprel.ec.europa.eu/qr/381667" \
    -o example.svg
```

#### JSON support
```shell
$ tyre-label --json '{
    "supplier": "Cool Tyre",
    "type_identifier": "94385300",
    "size": "185/75 R16",
    "tyre_class": "C2",
    "fuel_efficiency": "C",
    "wet_grip": "A",
    "roll_noise": 72,
    "noise_level": "A",
    "snow_grip": true,
    "ice_grip": true,
    "eprel_id": 381667,
    "eprel_link": "https://eprel.ec.europa.eu/qr/381667"
}' -o example.svg
```

## Support for PNG and PDF formats
You can use [`librsvg`](https://gitlab.gnome.org/GNOME/librsvg) to convert resulting SVG files into PNG (bitmap) or PDF files. It's also possible to specify a zoom factor with `-z 2.0` which can be useful for bitmaps. See `man rsvg-convert` for more details.

```shell
rsvg-convert -f png example.svg > example.png
```

```shell
rsvg-convert -f pdf example.svg > example.pdf
```

## License

Distributed under the MIT license. See [LICENSE](LICENSE) file for more details.


[1]: https://ec.europa.eu/info/energy-climate-change-environment/standards-tools-and-labels/products-labelling-rules-and-requirements/energy-label-and-ecodesign/energy-efficient-products/tyres_en
