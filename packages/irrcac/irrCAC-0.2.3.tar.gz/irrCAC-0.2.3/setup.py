# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['irrCAC']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=6.2,<7.0',
 'pandas>=1.3.5,<2.0.0',
 'pytest>=6.2.5,<7.0.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'irrcac',
    'version': '0.2.3',
    'description': 'Degree of agreement among raters.',
    'long_description': 'Chance-corrected Agreement Coefficients\n=======================================\n\n.. image:: https://readthedocs.org/projects/irrcac/badge/?version=latest\n  :target: https://irrcac.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n  :target: https://github.com/pre-commit/pre-commit\n  :alt: pre-commit\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :target: https://github.com/psf/black\n\nThe **irrCAC** is a Python package that provides several functions for\ncalculating various chance-corrected agreement coefficients. This package\nclosely follows the general framework of inter-rater reliability assessment\npresented by Gwet (2014).\n\nThe functionality covers calculations for various chance-corrected agreement\ncoefficients (CAC) among 2 or more raters. Among the CAC coefficients covered\nare Cohen\'s kappa, Conger\'s kappa, Fleiss\' kappa, Brennan-Prediger coefficient,\nGwet\'s AC1/AC2 coefficients, and Krippendorff\'s alpha. Multiple sets of weights\nare proposed for computing weighted analyses.\n\nThe functions included in this package can handle 2 types of input data. Those\ntypes with the corresponding coefficients are in the following list:\n\n1. Contingency Table\n\n  1. Brennar-Prediger\n  2. Cohen\'s kappa\n  3. Gwet AC1/AC2\n  4. Krippendorff\'s Alpha\n  5. Percent Agreement\n  6. Schott\'s Pi\n\n2. Raw Data\n\n  1. Fleiss\' kappa\n  2. Gwet AC1/AC2\n  3. Krippendorff\'s Alpha\n\n.. note::\n   All of these statistical procedures are described in details in\n   Gwet, K.L. (2014,ISBN:978-0970806284):\n   "Handbook of Inter-Rater Reliability," 4th edition, Advanced Analytics, LLC.\n\n   This package is a port *(with permission)* to Python of the\n   `irrCAC <https://github.com/kgwet/irrCAC>`_ library for R by Gwet, K.L.\n\n.. important::\n   This is a **work in progress** and *does not* have (yet) the full\n   functionality found in the R library.\n\nInstallation\n------------\nTo install the package, run:\n\n.. code:: bash\n\n    pip install irrCAC\n\nDevelopers\n----------\nTo run the tests, install `poetry <https://python-poetry.org/>`_ and run:\n\n.. code:: bash\n\n    poetry install\n\nNext run:\n\n.. code:: bash\n\n    poetry run pytest\n\nThere is also a config file for `tox <https://tox.readthedocs.io/en/latest/>`_\nso you can automatically run the tests for various python versions like this:\n\n.. code:: bash\n\n    tox\n\nDocumentation\n-------------\nThe documentation of the project is available at the following page:\nhttp://irrcac.readthedocs.io/\n',
    'author': 'Aris Fergadis',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/afergadis/irrCAC',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
