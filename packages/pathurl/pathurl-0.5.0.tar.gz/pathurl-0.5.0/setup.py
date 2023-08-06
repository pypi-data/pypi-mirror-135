# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pathurl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pathurl',
    'version': '0.5.0',
    'description': 'url manipulation',
    'long_description': '=============================\npathurl: object-oriented URLs\n=============================\n\n.. image:: https://github.com/spapanik/pathurl/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/pathurl/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/pathurl.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/pathurl/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/pathurl\n  :alt: License\n  :target: https://github.com/spapanik/pathurl/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/pathurl\n  :alt: PyPI\n  :target: https://pypi.org/project/pathurl\n.. image:: https://pepy.tech/badge/pathurl\n  :alt: Downloads\n  :target: https://pepy.tech/project/pathurl\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``pathurl`` is an objected-oriented way of manipulating URLs.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *pathurl* to them.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    pathurl = "^0.5.0"\n\nUsage\n^^^^^\n\n``pathurl`` offers classes to manipulate URLs, paths and query strings. All objects are immutable.\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/spapanik/pathurl/blob/main/CHANGELOG.rst\n.. _Documentation: https://pathurl.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/pathurl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
