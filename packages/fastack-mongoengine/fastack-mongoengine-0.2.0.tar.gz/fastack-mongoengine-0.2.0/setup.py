# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack_mongoengine']

package_data = \
{'': ['*']}

install_requires = \
['fastack>=4.0.0,<5.0.0', 'mongoengine>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'fastack-mongoengine',
    'version': '0.2.0',
    'description': 'MongoEngine integration for fastack',
    'long_description': "# fastack-mongoengine\n\n[MongoEngine](https://github.com/MongoEngine/mongoengine) integration for [fastack](https://github.com/fastack-dev/fastack).\n\n# Installation\n\n```\npip install fastack-mongoengine\n```\n\n# Usage\n\nAdd the plugin to your project configuration:\n\n```python\nPLUGINS = [\n    'fastack_mongoengine',\n    ...\n]\n```\n\nConfiguration:\n\n* ``MONGODB_URI``: MongoDB URI.\n",
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack-mongoengine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
