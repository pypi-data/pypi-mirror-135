# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turms',
 'turms.cli',
 'turms.parser',
 'turms.plugins',
 'turms.processor',
 'turms.types',
 'turms.wards']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'graphql-core>=3.2.0,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rich>=11.0.0,<12.0.0']

entry_points = \
{'console_scripts': ['turms = turms.cli.main:entrypoint']}

setup_kwargs = {
    'name': 'turms',
    'version': '0.1.12',
    'description': 'graphql-codegen powered by pydantic',
    'long_description': '# turms\n\n[![codecov](https://codecov.io/gh/jhnnsrs/turms/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/turms)\n[![PyPI version](https://badge.fury.io/py/turms.svg)](https://pypi.org/project/turms/)\n\n### DEVELOPMENT\n\n## Inspiration\n\nTurms is a pure python implementation of the awesome graphql-codegen library, following a simliar extensible design.\nIt makes heavy use of pydantic and its serialization capablities and provides fully typed querys, mutations and subscriptions\n\n## Supports\n\n- Documents\n- Fragments\n- Enums\n- Query Functions\n\n## Features\n\n- Fully Modular (agnostic of graphql engine)\n- Specify type mixins, baseclasses...\n- Fully Support type hints for variables (Pylance)\n\n## Installation\n\n```bash\npip install turms\n```\n\n## Usage\n\nOpen your workspace (create a virtual env), in the root folder\n\n```bash\nturms init\n```\n\nThis creates a configuration file in the working directory, edit this to reflect your\nsettings (see Configuration)\n\n```bash\nturms gen\n```\n\nGenerate beautifully typed Operations, Enums,...\n\n### Why Turms\n\nIn Etruscan religion, Turms (usually written as 𐌕𐌖𐌓𐌌𐌑 Turmś in the Etruscan alphabet) was the equivalent of Roman Mercury and Greek Hermes, both gods of trade and the **messenger** god between people and gods.\n',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
