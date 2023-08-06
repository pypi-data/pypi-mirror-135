# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack_sqlmodel']

package_data = \
{'': ['*']}

install_requires = \
['fastack>=4.0.0,<5.0.0', 'sqlmodel>=0.0.6,<0.0.7']

setup_kwargs = {
    'name': 'fastack-sqlmodel',
    'version': '0.4.0',
    'description': 'SQLModel integration for fastack',
    'long_description': "# fastack-sqlmodel\n\n[SQLModel](https://github.com/tiangolo/sqlmodel) integration for [fastack](https://github.com/fastack-dev/fastack).\n\n# Installation\n\n```\n$ pip install fastack-sqlmodel\n```\n\n# Usage\n\nAdd the plugin to your project configuration:\n\n```python\nPLUGINS = [\n    'fastack_sqlmodel',\n    ...\n]\n```\n\nConfiguration:\n\n* ``SQLALCHEMY_DATABASE_URI``: The database URI.\n* ``SQLALCHEMY_OPTIONS``: Additional parameters for the SQLAlchemy engine.\n",
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack-sqlmodel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
