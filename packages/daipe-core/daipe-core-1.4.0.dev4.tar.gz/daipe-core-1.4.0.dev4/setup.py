# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['daipecore',
 'daipecore.bootstrap',
 'daipecore.container',
 'daipecore.decorator',
 'daipecore.decorator.tests',
 'daipecore.function',
 'daipecore.function.input_decorator_function_basic_test',
 'daipecore.function.input_decorator_function_import_test',
 'daipecore.function.input_decorator_function_nested_test',
 'daipecore.lineage',
 'daipecore.lineage.argument',
 'daipecore.logger',
 'daipecore.pandas.dataframe',
 'daipecore.shortcut',
 'daipecore.test',
 'daipecore.widgets']

package_data = \
{'': ['*'], 'daipecore': ['_config/*']}

install_requires = \
['console-bundle>=0.5,<0.6',
 'injecta>=0.10.0,<0.11.0',
 'logger-bundle>=0.7.0,<0.8.0',
 'pandas>=1.0.1,<2.0.0',
 'pyfony-bundles>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['daipe = consolebundle.CommandRunner:run_command'],
 'pyfony.bundle': ['create = daipecore.DaipeCore:DaipeCore']}

setup_kwargs = {
    'name': 'daipe-core',
    'version': '1.4.0.dev4',
    'description': 'Daipe framework core',
    'long_description': '# Daipe Core\n\nCore component of the [Daipe Framework](https://www.daipe.ai).  \n\n## Resources\n\n* [Documentation](https://docs.daipe.ai/)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/daipe-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
