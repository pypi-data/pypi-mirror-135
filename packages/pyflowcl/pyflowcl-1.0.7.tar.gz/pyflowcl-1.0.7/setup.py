# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyflowcl']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyflowcl',
    'version': '1.0.7',
    'description': 'Cliente para comunicacion con flowAPI-3 de flow.cl',
    'long_description': 'PyFlowCL\n============\n\nCliente API para operaciones con el servicio de pagos Flow.cl  \n[FlowAPI-3.0.1](https://www.flow.cl/docs/api.html) \n\n---\n\n## Comandos Habilitados\n- [Payment](https://www.flow.cl/docs/api.html#tag/payment)\n- [Refund](https://www.flow.cl/docs/api.html#tag/refund)\n\n\n---\n\n## Instalacion\nEste proyecto está desarrollado para Python 3.7 y superior.  \nPara soporte Python 3.6 revisar la rama **stable-py36**.  \nEste proyecto es administrado por Poetry.  \nSe entrega archivo requirements.txt para PIP.  \nEjemplos en flow_client.py\n\n\n---\n\n## Uso\n```python\nfrom pyflowcl import Payment\nfrom pyflowcl.Clients import ApiClient\n\nAPI_URL = "https://sandbox.flow.cl/api"\nAPI_KEY = "your_key"\nAPI_SECRET = "your_secret"\nFLOW_TOKEN = "your_payment_token"\napi = ApiClient(API_URL, API_KEY, API_SECRET)\n\ncall = Payment.getStatus(api, FLOW_TOKEN)\nprint(call)\n```\n\n---\n\n## Licencia\n>Puedes revisar el texto completo de la licencia [aqui](https://github.com/mariofix/pyflowcl/blob/stable-v3/LICENSE)\n\nEste proyecto está licenciado bajo los términos de la licencia **MIT**.  \nFlowAPI está licenciado bajo los términos de la licencia **Apache 2.0**.\n  \n![Tests PyFlowCL](https://github.com/mariofix/pyflowcl/workflows/Test%20PyFlowCL/badge.svg)',
    'author': 'Mario Hernandez',
    'author_email': 'yo@mariofix.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mariofix/pyflowcl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
