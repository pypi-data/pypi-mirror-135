# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycep']

package_data = \
{'': ['*']}

install_requires = \
['lark>=1.0.0,<2.0.0', 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'pycep-parser',
    'version': '0.0.1a5',
    'description': 'A Python based Bicep parser',
    'long_description': '# pycep\n\n[![codecov](https://codecov.io/gh/gruebel/pycep/branch/master/graph/badge.svg?token=49WHVYGE1D)](https://codecov.io/gh/gruebel/pycep)\n[![PyPI](https://img.shields.io/pypi/v/pycep-parser)](https://pypi.org/project/pycep-parser/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycep-parser)](https://github.com/gruebel/pycep)\n\nA fun little project, which has the goal to parse\n[Azure Bicep](https://github.com/Azure/bicep) files.\nThis is still a very early stage, therefore a lot can and will change.\n\n## Next milestones\n\n### General\n- [x] Complete loop support\n- [x] Param decorator\n- [x] Resource/Module decorator\n- [x] Target scope\n- [ ] Existing resource keyword\n- [ ] Module alias\n- [ ] Deployment condition\n- [x] Adding line numbers to element blocks\n\n### Operators\n- [x] Comparison\n  - [x] Greater than or equals\n  - [x] Greater than\n  - [x] Less than or equals\n  - [x] Less than\n  - [x] Equals\n  - [x] Not equals\n  - [x] Equals case-insensitive\n  - [x] Not equals case-insensitive\n- [ ] Logical\n  - [ ] And\n  - [ ] Or\n  - [ ] Not\n  - [ ] Coalesce\n  - [x] Conditional expression\n\n### CI/CD\n- [x] Add test coverage\n\n## Considering\n- Adding line numbers to other parts\n\n## Out-of-scope\n- Bicep to ARM converter and vice versa\n',
    'author': 'Anton Grübel',
    'author_email': 'anton.gruebel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gruebel/pycep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
