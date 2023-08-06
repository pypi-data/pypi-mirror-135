# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack_migrate', 'fastack_migrate.templates.fastack']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.7.5,<2.0.0',
 'fastack-sqlmodel>=0.4.0,<0.5.0',
 'fastack>=4.0.0,<5.0.0']

entry_points = \
{'fastack.commands': ['db = fastack_migrate.cli:db']}

setup_kwargs = {
    'name': 'fastack-migrate',
    'version': '0.4.0',
    'description': 'Database migrations tool for Fastack',
    'long_description': '# fastack-migrate\n\nfastack-migrate is a database migration tool for [fastack](https://github.com/fastack-dev/fastack).\n\nThis is a fork of [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate)!\n\n# Usage\n\nInstall plugin:\n\n```\npip install -U fastack-migrate\n```\n\nAdd the plugin to your project configuration:\n\n```python\nPLUGINS = [\n    "fastack_sqlmodel",\n    "fastack_migrate",\n    ...\n]\n```\n\nAnd initialize your project with alembic template:\n\n```\nfastack db init\n```\n\nThen check if there are any changes in ``app.models``:\n\n```\nfastack db migrate\n```\n\nUpdate all changes in ``app.models``:\n\n```\nfastack db upgrade\n```\n\nFor more, please visit https://flask-migrate.readthedocs.io/en/latest/\n',
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack-migrate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
