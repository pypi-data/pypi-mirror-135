# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['afesta_tools', 'afesta_tools.lpeg']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'click>=8.0.1',
 'fake-winreg>=1.6.0,<2.0.0',
 'funcy>=1.17,<2.0',
 'loguru>=0.5.3,<0.6.0',
 'platformdirs>=2.4.1,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['afesta = afesta_tools.__main__:cli']}

setup_kwargs = {
    'name': 'afesta-tools',
    'version': '0.0.2',
    'description': 'Afesta Tools',
    'long_description': "Afesta Tools\n============\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\nLibrary and tools for AFesta.tv\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/afesta-tools.svg\n   :target: https://pypi.org/project/afesta-tools/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/afesta-tools.svg\n   :target: https://pypi.org/project/afesta-tools/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/afesta-tools\n   :target: https://pypi.org/project/afesta-tools\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/afesta-tools\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/afesta-tools/latest.svg?label=Read%20the%20Docs\n   :target: https://afesta-tools.readthedocs.io/\n   :alt: Read the documentation at https://afesta-tools.readthedocs.io/\n.. |Tests| image:: https://github.com/bhrevol/afesta-tools/workflows/Tests/badge.svg\n   :target: https://github.com/bhrevol/afesta-tools/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/bhrevol/afesta-tools/branch/main/graph/badge.svg\n   :target: https://app.codecov.io/gh/bhrevol/afesta-tools\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* Login to Afesta/LPEG API and register as a new player/client\n* Re-use existing 4D Media Player installation + login credentials when\n  available (Windows only)\n* Download Afesta videos via CLI (requires valid account and appropriate\n  purchases/permissions)\n\n\nRequirements\n------------\n\n* Python 3.8+\n* Valid Afesta account\n\n\nInstallation\n------------\n\nYou can install *Afesta Tools* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install afesta-tools\n\n\nUsage\n-----\n\nLogin to Afesta via CLI:\n\n.. code:: console\n\n    $ afesta login\n    Afesta username: username\n    Afesta password:\n\nDownload videos:\n\n.. code:: console\n\n    $ afesta dl m1234-0000 m1234-0000_1 m1234-0000_2 m1234-0000_3\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Afesta Tools* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/bhrevol/afesta-tools/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: https://afesta-tools.readthedocs.io/en/latest/contributing.html\n.. _Usage: https://afesta-tools.readthedocs.io/en/latest/usage.html\n",
    'author': 'byeonhyeok',
    'author_email': 'bhrevol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bhrevol/afesta-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
