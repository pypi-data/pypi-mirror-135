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
    'version': '0.1.1',
    'description': 'A developer centric, performant Python web framework',
    'long_description': '# xpresso\n\n[![codecov](https://codecov.io/gh/adriangb/xpresso/branch/main/graph/badge.svg?token=A0FXC8B93Y)](https://codecov.io/gh/adriangb/xpresso)\n![Test & Release](https://github.com/adriangb/xpresso/actions/workflows/workflow.yaml/badge.svg)\n\n## Introduction\n\nxpresso is an ASGI web framework built on top of [Starlette], [Pydantic] and [di], with heavy inspiration from [FastAPI].\n\nSome of the standout features are:\n\n- ASGI support for high performance (within the context of Python web frameworks)\n- OpenAPI documentation generation\n- Automatic parsing and validation of request bodies and parameters, with hooks for custom extractors\n- Full support for [OpenAPI parameter serialization](https://swagger.io/docs/specification/serialization/)\n- Highly typed and tested codebase with great IDE support\n- A powerful dependency injection system, backed by [di]\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n```shell\npip install xpresso\n```\n\nYou\'ll also want to install an ASGI server, such as [Uvicorn].\n\n```shell\npip install uvicorn\n```\n\n## Example\n\nCreate a file named `example.py`:\n\n```python\nfrom typing import List, Optional\nfrom pydantic import BaseModel\nfrom xpresso import App, PathItem, FromPath, FromQuery\n\nclass UserModel(BaseModel):\n    user_id: str\n    age: Optional[int] = None\n\nasync def get_users(\n    ids: FromPath[List[int]],\n    include_age: FromQuery[bool],\n) -> List[UserModel]:\n    if include_age:\n        return [UserModel(user_id=user_id, age=123) for user_id in ids]\n    return [UserModel(user_id=user_id) for user_id in ids]\n\napp = App(\n    routes=[\n        PathItem(\n            path="/users/{ids}",\n            get=get_users\n        )\n    ]\n)\n```\n\nRun the application:\n\n```shell\nuvicorn example:app\n```\n\nFor more examples, tutorials and reference materials, see our [documentation].\n\n[Starlette]: https://github.com/encode/starlette\n[Pydantic]: https://github.com/samuelcolvin/pydantic/\n[FastAPI]: https://github.com/tiangolo/fastapi\n[di]: https://github.com/adriangb/di\n[Uvicorn]: http://www.uvicorn.org/\n[documentation]: https://www.adriangb.com/xpresso/\n\nSee this release on GitHub: [v0.1.1](https://github.com/adriangb/di/releases/tag/0.1.1)\n',
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
