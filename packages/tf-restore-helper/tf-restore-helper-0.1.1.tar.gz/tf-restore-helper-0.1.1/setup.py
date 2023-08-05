# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tf_restore_helper']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17,<1.21',
 'click-logging>=1.0,<1.1',
 'click>=7,<9',
 'coloredlogs>=15.0,<15.1',
 'flatplan>=1.3,<1.4']

entry_points = \
{'console_scripts': ['tf-restore-helper = tf_restore_helper.__main__:main']}

setup_kwargs = {
    'name': 'tf-restore-helper',
    'version': '0.1.1',
    'description': 'Tf Restore Helper',
    'long_description': 'Tf Restore Helper\n=================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/tf-restore-helper.svg\n   :target: https://pypi.org/project/tf-restore-helper/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/tf-restore-helper\n   :target: https://pypi.org/project/tf-restore-helper\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/tf-restore-helper\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/tf-restore-helper/latest.svg?label=Read%20the%20Docs\n   :target: https://tf-restore-helper.readthedocs.io/\n   :alt: Read the documentation at https://tf-restore-helper.readthedocs.io/\n.. |Tests| image:: https://github.com/dogfish182/tf-restore-helper/workflows/Tests/badge.svg\n   :target: https://github.com/dogfish182/tf-restore-helper/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/dogfish182/tf-restore-helper/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/dogfish182/tf-restore-helper\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n\n* Constructs Terraform import commands to assist an operator aligning a terraform state after volume restores have taken place by an external tool, which results in terraform misalignment.\n\n* Tool is currently only compatible with AWS volumes (PRs welcome) and is used at own risk. Operators that do not understand the terraform state file or what the produced commands will do, should not use this tool as a helper and proper state backup and recovery procedures should be well understood before making use of this.\n\n\nInstallation\n------------\n\nYou can install *Tf Restore Helper* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install tf-restore-helper\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\nExamples of usage:\n\n.. code:: console\n\n   > tf-restore-helper --planfile tests/assets/plan.json\n    2021-05-03 13:28:43 sbpltc1nplvdl botocore.credentials[79705] INFO Found credentials in environment variables.\n    2021-05-03 13:28:46 sbpltc1nplvdl postrestoretfcli[79705]   WARNING THIS INFORMATION SHOULD BE USED ONLY IF YOU KNOW WHAT YOU ARE DOING!\n    -----------Terraform volume alignment commands-----------\n    terraform state rm "aws_ebs_volume.test-instance-volume-1"\n    terraform state rm "aws_volume_attachment.test-instance-volume-1"\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Tf Restore Helper* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/dogfish182/tf-restore-helper/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://tf-restore-helper.readthedocs.io/en/latest/usage.html\n',
    'author': 'Gary Hawker',
    'author_email': 'dogfish@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dogfish182/tf-restore-helper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
