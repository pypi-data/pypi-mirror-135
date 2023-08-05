# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyanalyst6api']

package_data = \
{'': ['*']}

install_requires = \
['pytus>=0.2.1,<0.3.0', 'requests>=2.27,<3.0']

setup_kwargs = {
    'name': 'polyanalyst6api',
    'version': '0.23.2',
    'description': 'polyanalyst6api is a PolyAnalyst API client for Python.',
    'long_description': '# polyanalyst6api\n\n[![PyPI package](https://img.shields.io/pypi/v/polyanalyst6api.svg?)](https://pypi.org/project/polyanalyst6api)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/polyanalyst6api.svg?)](https://pypi.org/project/polyanalyst6api/)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Megaputer/polyanalyst6api-python/blob/master/LICENSE)\n\n`polyanalyst6api` is a Python library for interacting with PolyAnalyst APIs.\n\nThis package provides easy to use wrappers for PolyAnalyst `Analytical Client`, `Scheduler` and `Drive`.\nWith it you can execute nodes, view datasets, run tasks, download/upload files and so on.\n\n## Installation\n\nPython 3.6+ is required. Install, upgrade and uninstall `polyanalyst6api-python` with these commands:\n\n```\n$ pip install polyanalyst6api\n$ pip install --upgrade polyanalyst6api\n$ pip uninstall polyanalyst6api\n```\n\n## Documentation\n\nSee [API Reference](https://megaputer.github.io/polyanalyst6api-python/) for the library methods.\n\nRefer to **PolyAnalyst User Manual** at **Application Programming Interfaces** > **Version 01** for\nREST API specification.\n\n## Usage\n\n### Authentication\n\nFrom version `0.23.0` you can use the configuration file to store your credentials. By default, its location is\n`C:\\Users\\_user_\\.polyanalyst6api\\config` (`~/.polyanalyst6api/config` in linux).\n\nAt a minimum, the credentials file should specify the url and credentials keys. You may also want to add a `ldap_server`\nif you\'re logging in via LDAP. All other keys or sections except `DEFAULT` are ignored.\n\n```ini\n[DEFAULT]\nurl=POLYANALYST_URL\nusername=YOUR_USERNAME\npassword=YOUR_PASSWORD\nldap_server=LDAP\n```\n\nAfter creating the configuration file you can use `API` context manager to automatically log in to and log out\nfrom PolyAnalyst server:\n\n```python\nwith polyanalyst6api.API() as api:\n    ...\n```\n\nAlternatively, you can pass an url, credentials and ldap_server when creating api client. In this case arguments\nwill be used over values from the configuration file.\n```python\nwith polyanalyst6api.API(POLYANALIST_URL, YOUR_USERNAME, YOUR_PASSWORD) as api:\n    ...\n```\n\n### Working with project\n\nInstantiate project wrapper by calling with existing project ID:\n```python\nprj = api.project(PROJECT_UUID)\n```\n\nSet `Python` node code using parent `Parameters` node.\n```python\nprj.parameters(\'Parameters (1)\').set(\n    \'Dataset/Python\',\n    {\'Script\': \'result = pandas.DataFrame([{"val": 42}])\'}\n)\n```\n\nExecute `Python` node and wait to complete execution\n```python\nprj.execute(\'Python\', wait=True)\n```\n\nCheck node results:\n```python\nds = prj.dataset(\'Python\').preview()\nassert ds[0][\'val\'] == 42\n```\n\nSave project:\n```python\nprj.save()\n```\n\n### Downloading file from user home folder using PA Drive API\n\n```python\ncontent = api.drive.download_file(\'README.txt\')\nwith open(r\'C:\\README.txt\', mode=\'wb+\') as local_file:\n    local_file.write(content)\n```\n\nSee [polyanalyst6api-python/examples](https://github.com/Megaputer/polyanalyst6api-python/tree/master/examples) for more complex examples.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'yatmanov',
    'author_email': 'yatmanov@megaputer.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Megaputer/polyanalyst6api-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
