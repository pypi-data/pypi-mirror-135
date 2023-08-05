# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeline_runner', 'pipeline_runner.static']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'boto3>=1.16.63,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'coloredlogs>=15.0,<16.0',
 'cryptography>=3.4.8,<4.0.0',
 'docker>=5.0.2,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyfzf>=0.2.2,<0.3.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'python-slugify>=5.0.2,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'tenacity>=7.0.0,<8.0.0']

entry_points = \
{'console_scripts': ['pipeline-runner = pipeline_runner.cli:main']}

setup_kwargs = {
    'name': 'bitbucket-pipeline-runner',
    'version': '0.3.4',
    'description': 'Run a bitbucket pipeline locally',
    'long_description': "# Bitbucket Pipeline Runner\n\nTool to run Bitbucket Pipelines locally.\n\n## Installation\n```shell\npip install bitbucket-pipeline-runner\n```\n\n## Basic usage\nTo run a pipeline\n```shell\ncd <project-directory>\npipeline-runner run <pipeline-name>\n```\n\nTo list available pipelines\n```shell\ncd <project-directory>\npipeline-runner list\n```\n\n## Environment variables\nbitbucket pipeline runner already sets all `BITBUCKET_*` enviromnent variables in the step's run enviromnent.\nIt will also source any `.env` file in the current directory, for all project specific enviromnent variables.\n\n## Artifacts and logs\nPersistent data like artifacts generated from your pipelines and execution logs can be found in your user's data directory.\n\nOn Linux:\n\n    ${XDG_DATA_HOME:-~/.local/share}/pipeline-runner\n\nOn macOS:\n\n    ~/Library/Application Support/pipeline-runner\n\n## Caches\nCaches defined in your pipelines are stored in your user's cache directory.\n\nOn Linux:\n\n    ${XDG_CACHE_HOME:-~/.cache}/pipeline-runner\n\nOn macOS:\n\n    ~/Library/Caches/pipeline-runner\n",
    'author': 'Mathieu Lemay',
    'author_email': 'acidrain1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mathieu-lemay/pipeline-runner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
