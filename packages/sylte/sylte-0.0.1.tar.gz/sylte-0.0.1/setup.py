# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sylte']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'sylte',
    'version': '0.0.1',
    'description': 'Pickling and unpickling of function arguments',
    'long_description': "# sylte\n\n![Testing and linting](https://github.com/danhje/sylte/workflows/Test%20And%20Lint/badge.svg)\n[![codecov](https://codecov.io/gh/danhje/sylte/branch/master/graph/badge.svg)](https://codecov.io/gh/danhje/sylte)\n![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/danhje/sylte?include_prereleases)\n![PyPI](https://img.shields.io/pypi/v/sylte)\n\nSylte provides a decorator that stores function arguments as a pickle file in a central location,\nand functions for retrieving those arguments later on, so that the function can be re-invoked\nwith the same args. Useful when writing or debugging a function that exists somewhere near the end\nof a long-running pipeline.\n\n## Installation\n\nUsing poetry:\n\n```shell\npoetry add sylte\n```\n\nUsing pipenv:\n\n```shell\npipenv install sylte\n```\n\nUsing pip:\n\n```shell\npip install sylte\n```\n\n## Usage\n\nLet's say we have a function `transform` that we want to debug or modify. We will have to call it\nseveral times to see how it behaves with real data. It's normally called as part of a long-running\npipeline, and we don't want to have to wait for this pipeline every time. We could write a unit-test,\nbut perhaps we aren't yet sure how the output will look, and perhaps the input-data is complex\nand time-consuming to recreate in a test, and we'd prefer to do that when the function is finalized,\nto avoid having to repeatedly modify the test as the function is modified.\n\nEnter sylte. By applying the `@sylt` decorator to the function and running the pipeline once,\nthe args are recorded, and can be retrieved later.\n\n```python\nfrom sylte import sylt\n\n@sylt\ndef transform(this_huge_df, this_other_huge_df, this_object_with_lots_of_attributes):\n    ...\n```\n\nThe arg set will be stored in a pickle file in the default cache location for the os.\nThe location can be seen by running `from sylte import CACHE_DIR; print(CACHE_DIR)`.\nTo use a different location than the default, specify the location with the environment variable `SYLTE_CACHE_DIR`.\n\nThe file name will have the format\n`<file name>-<function name>-<timestamp>.pickle`.\n\nThe function `latest` will retrieve an unsylt the latest arg set, returning a tuple with args and kwargs.\n\n```python\n>>> from sylte import latest\n...\n>>> args, kwargs = latest()\n>>> transform(*args, **kwargs)\n```\n\n`show` returns a list of all sylted arg sets:\n\n```python\n>>> from sylte import show\n...\n>>> show()\n['demo-transform-2022-01-14-15-08-59',\n 'demo-transform-2022-01-14-15-12-33',]\n```\n\n`unsylt` unsylts and returns the arg set with the specified name as output by `show`, i.e. the filename with the extension omitted:\n\n```python\n>>> from sylte import unsylt\n...\n>>> args, kwargs = unsylt('demo-add-2022-01-14-15-08-59')\n>>> transform(*args, **kwargs)\n```\n\n`clear` deletes all previously sylted arg sets:\n\n```python\n>>> from sylte import clear, show\n...\n>>> clear()\n>>> show()\n[]\n```\n",
    'author': 'Daniel Hjertholm',
    'author_email': 'daniel.hjertholm@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danhje/sylte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
