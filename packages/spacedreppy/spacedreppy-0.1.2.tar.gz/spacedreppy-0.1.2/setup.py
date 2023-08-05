# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacedreppy', 'spacedreppy.memory_models', 'spacedreppy.schedulers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spacedreppy',
    'version': '0.1.2',
    'description': 'A spaced repetition Python library.',
    'long_description': '\n# SpacedRepPy\n\n<div style="text-align: center">\n\n[![Build status](https://github.com/lschlessinger1/spacedreppy/workflows/build/badge.svg?branch=main&event=push)](https://github.com/lschlessinger1/spacedreppy/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/spacedreppy.svg)](https://pypi.org/project/spacedreppy/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/lschlessinger1/spacedreppy/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/lschlessinger1/spacedreppy/blob/main/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/lschlessinger1/spacedreppy/releases)\n[![License](https://img.shields.io/github/license/lschlessinger1/spacedreppy)](https://github.com/lschlessinger1/spacedreppy/blob/main/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n\nA spaced repetition Python library.\n\n</div>\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install `spacedreppy`.\n\n```bash\npip install spacedreppy\n```\n\n## Usage\n\n```python\nfrom datetime import datetime\nfrom spacedreppy.schedulers.sm2 import SM2Scheduler\n\n# returns next due timestamp and next interval.\nscheduler = SM2Scheduler()\ndue_timestamp, interval = scheduler.compute_next_due_interval(attempted_at=datetime.utcnow(), result=3)\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Louis Schlessinger',
    'author_email': '2996982+lschlessinger1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
