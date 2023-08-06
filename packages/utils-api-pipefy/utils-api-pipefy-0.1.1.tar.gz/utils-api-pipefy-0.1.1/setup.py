# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utils_api_pipefy', 'utils_api_pipefy.libs']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.19.0,<0.20.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'utils-api-pipefy',
    'version': '0.1.1',
    'description': 'Ferramentas de para otimizar o consumo de api do pipefy, trantando os retornos e criando concurrence futures para multi-processamentos.',
    'long_description': None,
    'author': 'Yuri Motoshima',
    'author_email': 'yurimotoshima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
