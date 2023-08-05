# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chocs_middleware', 'chocs_middleware.xray']

package_data = \
{'': ['*']}

install_requires = \
['aws-xray-sdk>=2.9.0,<3.0.0', 'chocs>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'chocs-middleware.xray',
    'version': '1.0.0',
    'description': 'Middleware to integrate aws x-ray with chocs.',
    'long_description': '# chocs-aws-xray\nAWS X-Ray middleware for chocs library.\n\n## Installation \nthrough poetry:\n```shell\npoetry add chocs_middleware.xray\n```\nor through pip:\n```shell\npip install chocs_middleware.xray\n```\n\n## Usage\n\nThe following snippet is the simplest integration example.\n\n> Please note x-ray won\'t work in WSGI mode, it has to be deployed as aws lambda in order to work.\n> \n```python\nfrom chocs import Application, HttpResponse, serve\nfrom chocs_middleware.xray import AwsXRayMiddleware\n\napp = Application(AwsXRayMiddleware())\n\n\n@app.get("/hello")\ndef say_hello(request):\n    return HttpResponse("Hello")\n\nserve(app)\n```\n\n### Setting up custom error handler\n\nAWS X-Ray middleware provides a way to setup a custom error handler which may become handy when you\nneed to supplement your logs with additional information. Please consider the following example:\n\n```python\nfrom chocs import Application, HttpResponse, HttpStatus\nfrom chocs_middleware.xray import AwsXRayMiddleware\n\ndef error_handler(request, error, segment):\n    segment.add_exception(error)\n    \n    return HttpResponse("NOT OK", HttpStatus.INTERNAL_SERVER_ERROR)\n\napp = Application(AwsXRayMiddleware(error_handler=error_handler))\n\n\n@app.get("/hello")\ndef say_hello(request):\n    raise Exception("Not Today!")\n    return HttpResponse("Hello")\n\n```\n\n> To learn more about error_handler interface please click [here.]("./chocs_middleware/xray/middleware.py:16") \n\n### Accessing x-ray recorded from within your application layer\n```python\nfrom chocs import Application, HttpResponse\nfrom chocs_middleware.xray import AwsXRayMiddleware\n\napp = Application(AwsXRayMiddleware())\n\n@app.get("/hello")\ndef say_hello(request):\n    xray_recorder = request.attributes["aws_xray_recorder"] # Here is the instance of your recorder.\n    \n    return HttpResponse("OK")\n\n```\n\nThat\'s all.\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kodemore/chocs-aws-xray',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
