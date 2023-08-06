# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fbv']

package_data = \
{'': ['*']}

install_requires = \
['django-jsonview>=2.0.0,<3.0.0', 'django>2.2.0']

extras_require = \
{'docs': ['Sphinx>=4.3.2,<5.0.0',
          'linkify-it-py>=1.0.3,<2.0.0',
          'myst-parser>=0.16.1,<0.17.0',
          'furo>=2021.11.23,<2022.0.0',
          'sphinx-copybutton>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'django-fbv',
    'version': '0.1.0',
    'description': 'Utilities to make function-based views cleaner, more efficient, and better tasting. ',
    'long_description': "# django-fbv\n\nUtilities to make Django function-based views cleaner, more efficient, and better tasting.\n\n## decorators\n\n- `fbv.decorators.render_html`: convenience decorator to use instead of `django.shortcut.render` with a specified template\n- `fbv.decorators.render_view`: convenience decorator to use instead of `django.shortcut.render` with a specified template and content type\n\n## views\n\n- `fbv.views.html_view`: directly renders a template from `urls.py`\n\n## middleware\n\n- `fbv.middleware.RequestMethodMiddleware`: adds a boolean property to the `request` for the current request's HTTP method\n\nComplete documentation: https://django-fbv.readthedocs.org\n",
    'author': 'adamghill',
    'author_email': 'adam@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adamghill/django-fbv/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
