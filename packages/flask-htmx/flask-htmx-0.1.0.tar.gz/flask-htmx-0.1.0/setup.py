# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_htmx']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'flask-htmx',
    'version': '0.1.0',
    'description': 'A Flask extension to work with HTMX.',
    'long_description': '# Flask-HTMX\n\nA Flask extension to work with HTMX.\n',
    'author': 'Edmond Chuc',
    'author_email': 'edmond.chuc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/edmondchuc/flask-htmx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
