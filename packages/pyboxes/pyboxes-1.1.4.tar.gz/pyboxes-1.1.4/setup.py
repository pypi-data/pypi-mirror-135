# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyboxes', 'pyboxes.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'loguru>=0.5.3,<0.6.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['pybox = pyboxes.__main__:main']}

setup_kwargs = {
    'name': 'pyboxes',
    'version': '1.1.4',
    'description': 'Pyboxes',
    'long_description': '# Pybox\n\n<div align="center">\n\n<img src="https://raw.githubusercontent.com/cauliyang/pybox/main/docs/_static/logo.png" width=50% alt="logo">\n\n[![pypi](https://img.shields.io/pypi/v/pyboxes.svg)](https://pypi.org/project/pyboxes/)\n[![status](https://img.shields.io/pypi/status/pyboxes.svg)](https://pypi.org/project/pyboxes/)\n[![python version](https://img.shields.io/pypi/pyversions/pyboxes)](https://pypi.org/project/pyboxes)\n[![license](https://img.shields.io/pypi/l/pyboxes)](https://opensource.org/licenses/MIT)\n[![read the docs](https://img.shields.io/readthedocs/pyboxes/latest.svg?label=Read%20the%20Docs)](https://pyboxes.readthedocs.io/)\n\n[![test](https://github.com/cauliyang/pybox/workflows/Tests/badge.svg)](https://github.com/cauliyang/pybox/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/cauliyang/pybox/branch/main/graph/badge.svg)](https://codecov.io/gh/cauliyang/pybox)\n[![precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n</div>\n\n## Aims\n\n![feature1](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/20211205150625.png)\n\n- **Simple**: A simple and easy to use Python library for many annoy task.\n- **Easy to use**: Easy to use, you can use it in your project.\n- **extendable**: Extendable, you can add your own function easily.\n\n## Features\n\n<details>\n\n<summary> Google Driver</summary>\n\n[Google-Driver]: A simple and easy to download files by sharing link of Google Driver.\n\nFor example:\n\n```bash\n$ pybox gdriver <url> <name> <size>\n```\n\nDetailed usage please see [Usage Documentation]\n\n</details>\n\n<details>\n\n<summary> Slack</summary>\n\n[Slack]: A simple and easy to send message to Slack Channel.\n\nFor example:\n\n```bash\n$ pybox slack [options] <webhook-url>\n```\n\nDetailed usage please see [Usage Documentation]\n\n</details>\n\n- More to come...\n\n## Installation\n\nYou can install _Pybox_ via [pip] from [PyPI]:\n\n```bash\n$ pip install pyboxes\n```\n\n## Usage\n\n```bash\n$ pybox -h\n```\n\nPlease see the Command-line Reference [Usage] for details.\n\n## Contributing\n\nContributions are very welcome. To learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license],\n_Pybox_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[//]: # "link"\n[cjolowicz]: https://github.com/cjolowicz\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[mit license]: https://opensource.org/licenses/MIT\n[pypi]: https://pypi.org/\n[file an issue]: https://github.com/cauliyang/pybox/issues\n[pip]: https://pip.pypa.io/\n[google-driver]: https://www.google.com/drive/\n[usage]: https://pyboxes.readthedocs.io/en/latest/usage.html\n[slack]: https://slack.com/\n\n% github-only\n\n[contributor guide]: CONTRIBUTING.md\n[usage documentation]: https://pyboxes.readthedocs.io/en/latest/usage.html\n',
    'author': 'yangli',
    'author_email': 'li002252@umn.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cauliyang/pybox',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
