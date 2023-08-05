# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datanommer', 'datanommer.commands']

package_data = \
{'': ['*']}

install_requires = \
['datanommer.models>=1.0.0,<2.0.0', 'fedora-messaging>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['datanommer-create-db = datanommer.commands:create',
                     'datanommer-dump = datanommer.commands:dump',
                     'datanommer-latest = datanommer.commands:latest',
                     'datanommer-stats = datanommer.commands:stats']}

setup_kwargs = {
    'name': 'datanommer.commands',
    'version': '1.0.0',
    'description': 'Console commands for datanommer',
    'long_description': 'datanommer.commands\n===================\n\n.. split here\n\nThis package contains the console commands for datanommer, including::\n\n - datanommer-create-db\n - datanommer-dump\n - datanommer-stats\n\nDatanommer is a storage consumer for the Fedora Infrastructure Message Bus\n(fedmsg).  It is comprised of a `fedmsg <http://fedmsg.com>`_ consumer that\nstuffs every message into a sqlalchemy database.\n',
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/datanommer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
