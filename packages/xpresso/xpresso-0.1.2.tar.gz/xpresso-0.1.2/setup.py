# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpresso',
 'xpresso._extractors',
 'xpresso._extractors.body',
 'xpresso._extractors.params',
 'xpresso._openapi_providers',
 'xpresso._openapi_providers.body',
 'xpresso._openapi_providers.params',
 'xpresso._security',
 'xpresso._utils',
 'xpresso.dependencies',
 'xpresso.experimental',
 'xpresso.openapi']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3,<4', 'di>=0.38,<0.39', 'pydantic>=1,<2', 'starlette>=0.16.0,<2']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3'],
 ':python_version < "3.9"': ['typing-extensions>=3']}

setup_kwargs = {
    'name': 'xpresso',
    'version': '0.1.2',
    'description': 'A developer centric, performant Python web framework',
    'long_description': '<p align="center">\n  <a href="https://adriangb.com/xpresso"><img src="https://adriangb.com/xpresso/xpresso-with-title.png" alt="Xpresso"></a>\n</p>\n\n<p align="center">\n<a href="https://github.com/adriangb/xpresso/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/adriangb/xpresso/actions/workflows/workflow.yaml/badge.svg?event=push&branch=main" alt="Test">\n</a>\n<a href="https://codecov.io/gh/adriangb/xpresso" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/adriangb/xpresso?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/xpresso" target="_blank">\n    <img src="https://img.shields.io/pypi/v/xpresso?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/xpresso" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/xpresso.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n## Introduction\n\nxpresso is an ASGI web framework built on top of [Starlette], [Pydantic] and [di], with heavy inspiration from [FastAPI].\n\nSome of the standout features are:\n\n- ASGI support for high performance (within the context of Python web frameworks)\n- OpenAPI documentation generation\n- Automatic parsing and validation of request bodies and parameters, with hooks for custom extractors\n- Full support for [OpenAPI parameter serialization](https://swagger.io/docs/specification/serialization/)\n- Highly typed and tested codebase with great IDE support\n- A powerful dependency injection system, backed by [di]\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n```shell\npip install xpresso\n```\n\nYou\'ll also want to install an ASGI server, such as [Uvicorn].\n\n```shell\npip install uvicorn\n```\n\n## Example\n\nCreate a file named `example.py`:\n\n```python\nfrom pydantic import BaseModel\nfrom xpresso import App, Path, FromPath, FromQuery\n\nclass Item(BaseModel):\n    item_id: int\n    name: str\n\nasync def read_item(item_id: FromPath[int], name: FromQuery[str]) -> Item:\n    return Item(item_id=item_id, name=name)\n\napp = App(\n    routes=[\n        Path(\n            "/items/{item_id}",\n            get=read_item,\n        )\n    ]\n)\n```\n\nRun the application:\n\n```shell\nuvicorn example:app\n```\n\nFor more examples, tutorials and reference materials, see our [documentation].\n\n[Starlette]: https://github.com/encode/starlette\n[Pydantic]: https://github.com/samuelcolvin/pydantic/\n[FastAPI]: https://github.com/adriangb/xpresso\n[di]: https://github.com/adriangb/di\n[Uvicorn]: http://www.uvicorn.org/\n[documentation]: https://www.adriangb.com/xpresso/\n\nSee this release on GitHub: [v0.1.2](https://github.com/adriangb/di/releases/tag/0.1.2)\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'adrian@adriangb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adriangb/xpresso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
