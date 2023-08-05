# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jml']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jml = jml.jml:main']}

setup_kwargs = {
    'name': 'jml',
    'version': '0.2.0',
    'description': 'Ein Tool um Projektversionen zu generieren',
    'long_description': '===\njml\n===\n\n\nInstallation\n============\n\nDie Installation wird wie gewohnt mit pypi durchgeführt:\n\n.. code-block:: console\n\n   $ pip3 install jml\n\nBei erfolgreicher Installation ist nun das ``jml`` Kommando verfügbar.\n\n.. code-block:: console\n\n   $ jml --version\n   jml, version 0.2.0\n',
    'author': 'J. Neugebauer',
    'author_email': 'ngb@helmholtz-bi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/jneug/jml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
