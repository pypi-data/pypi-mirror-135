# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jcs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jcs',
    'version': '0.2.0',
    'description': 'JSC - JSON Canonicalization',
    'long_description': '# JCS - JSON Canonicalization for Python 3\n\n[![Tests](https://github.com/titusz/jcs/actions/workflows/tests.yml/badge.svg)](https://github.com/titusz/jcs/actions/workflows/tests.yml)\n\nThis is a Python 3 package for\na [JCS (RFC 8785)](https://datatracker.ietf.org/doc/html/rfc8785) compliant JSON\ncanonicalization.\n\nThe main author of this code is [Anders Rundgren](https://github.com/cyberphone). The\noriginal source code is\nat [cyberphone/json-canonicalization](https://github.com/cyberphone/json-canonicalization/tree/master/python3)\nincluding comprehensive test data.\n\n## Installation\n\n```bash\n$ pip install jcs\n```\n\n## Using JCS\n\n```python\nimport jcs\ndata = jcs.canonicalize({"tag": 4})\n```\n\n## Changelog\n\n### 0.2.0 - 2022-01-19\n\n- Removed pinning to py3\n- Updated dependencies\n\n### 0.1.0 - 2021-12-26\n\n- created `jcs` package from original code\n- added poetry based packaging\n- reformated code with `black`\n- add github ci testing workflow\n',
    'author': 'titusz',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/titusz/jcs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
