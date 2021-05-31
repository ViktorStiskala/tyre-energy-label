from setuptools import setup
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

entry_points = """\
[console_scripts]
tyre-label=tyre_label.cli:cli
"""

with open(ROOT_DIR / 'README.md', 'r') as f_readme:
    long_description = f_readme.read()

setup(
    name="tyre-energy-label",
    version="0.1.6",
    packages=["tyre_label"],
    package_data={'tyre_label': ['tyre_label/templates/*']},
    include_package_data=True,
    install_requires=["qrcode>=3.0.0", "jinja2>=2.9"],
    license='MIT',
    description='EU tyres energy label generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ViktorStiskala/tyre-energy-label',
    author='Viktor Stískala',
    author_email='viktor@stiskala.cz',
    entry_points=entry_points,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
