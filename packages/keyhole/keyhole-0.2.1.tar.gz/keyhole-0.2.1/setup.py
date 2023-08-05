# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keyhole', 'keyhole.mosaick', 'keyhole.register']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20,<2.0',
 'pyvips>=2.1.15,<3.0.0',
 'scikit-image>=0.18,<0.19',
 'scipy>=1.7,<2.0',
 'tqdm>=4.62.0,<5.0.0']

entry_points = \
{'console_scripts': ['keyhole = keyhole.cli:main']}

setup_kwargs = {
    'name': 'keyhole',
    'version': '0.2.1',
    'description': 'Work with declassified keyhole satellite images.',
    'long_description': '=======\nkeyhole\n=======\n\nA library and command-line tools for manipulating declassified imagery.\n\nThe primary use for this right now is mosaicking the separate "panel"\nscans of declassified imagery from EarthExplorer.\n\n\nUsage\n=====\n\nThere are two steps to mosaick the panel images:\n\n1.  Use the ``register`` subcommand to measure the panels\' overlap. This\n    will typically look something like::\n\n        keyhole register -j coreg.json name_*.tif\n\n    This will create ``coreg.json`` with the overlap information.\n\n2.  Then use the ``mosaick`` subcommand with the information generated in the\n    previous step to combine the images::\n\n        keyhole mosaick -o output.tif -j coreg.json name_*.tif\n\nThe ``shrink`` argument is useful for creating smaller preview images::\n\n    keyhole mosaick -o out.jpg --shrink 10 -j coreg.json name_*.tif\n\nTo create tiled pyramidal images::\n\n    keyhole mosaick -o out.tif \\\n        --tile --pyramid --tile_width 256 --tile_height 256 \\\n        -j coreg.json name_*.tif\n\nFor more information, see ``keyhole -h``.\n\n\nInstallation\n============\n\n**Before installation**, you must have libvips installed. The procedure for\nthat varies by platform; see `the libvips documentation`__ for more info.\nAfter that, simply::\n\n    pip install keyhole\n\n__ https://github.com/libvips/pyvips#non-conda-install\n\nThis installs both the package and the command-line tool ``keyhole``.\n\nYou can also run the code as a python module with ``python -m keyhole``.\n\nIf you\'ve cloned the ``keyhole`` repo and you have the dependencies described\nin ``pyproject.toml``, you can simply run the script at the root of the repo::\n\n    python keyhole.py -h\n\n',
    'author': 'Seth Warn',
    'author_email': 'swarn@uark.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
