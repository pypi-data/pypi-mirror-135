# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nldi_xstool', 'nldi_xstool.process']

package_data = \
{'': ['*']}

install_requires = \
['Bottleneck>=1.3.2,<2.0.0',
 'OWSLib>=0.25.0,<0.26.0',
 'click<8',
 'dask>=2021.11.2,<2022.0.0',
 'dataretrieval>=0.7,<0.8',
 'lxml>=4.6.4,<5.0.0',
 'netCDF4>=1.5.8,<2.0.0',
 'numpy>=1.21.0,<2.0.0',
 'py3dep',
 'pygeoapi>=0.11.0,<0.12.0',
 'pygeohydro',
 'pygeoogc==0.11.4',
 'pygeoutils',
 'pynhd',
 'scipy>=1.7.3,<2.0.0',
 'xarray>=0.20.1,<0.21.0']

entry_points = \
{'console_scripts': ['nldi-xstool = nldi_xstool.__main__:main']}

setup_kwargs = {
    'name': 'nldi-xstool',
    'version': '0.12.0.dev0',
    'description': 'Nldi Xstool',
    'long_description': "# Nldi Xstool\n\n[![PyPI](https://img.shields.io/pypi/v/nldi-xstool.svg)](https://pypi.org/project/nldi-xstool/)\n[![Status](https://img.shields.io/pypi/status/nldi-xstool.svg)](https://pypi.org/project/nldi-xstool/)\n[![Python Version](https://img.shields.io/pypi/pyversions/nldi-xstool)](https://pypi.org/project/nldi-xstool)\n[![License](https://img.shields.io/pypi/l/nldi-xstool)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)\n\n[![Read the documentation at https://nldi-xstool.readthedocs.io/](https://img.shields.io/readthedocs/nldi-xstool/latest.svg?label=Read%20the%20Docs)](https://nldi-xstool.readthedocs.io/)\n\n[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool/-/commits/main)\n[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool/-/commits/main)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)\n[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install nldi-xstool via\n[pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):\n\n```python\npip install nldi-xstool\n```\n\n## Command Line Usage\n\nPlease see the {doc}`usage`\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the {doc}`contributing`.\n\n## License\n\nDistributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode),\n_Nldi Xstool_ is free and open source software.\n\n## Disclaimer\n\n{doc}`disclaimer`\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool/-/issues) along with a detailed description.\n\n## Credits\n\nThis project was generated from\n[@hillc-usgs](https://github.com/hillc-usgs)'s [Pygeoapi Plugin\nCookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter)\ntemplate.\n",
    'author': 'Richard McDonald',
    'author_email': 'rmcd@usgs.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<3.10.0',
}


setup(**setup_kwargs)
