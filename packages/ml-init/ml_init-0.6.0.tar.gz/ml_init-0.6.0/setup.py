# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_init']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.12b0,<22.0',
 'datasets>=1.17.0,<2.0.0',
 'flake8>=4.0.1,<5.0.0',
 'hdbscan>=0.8.27,<0.9.0',
 'imbalanced-learn>=0.9.0,<0.10.0',
 'jupyter>=1.0.0,<2.0.0',
 'lightgbm>=3.3.2,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'mlflow>=1.22.0,<2.0.0',
 'notebook>=6.4.7,<7.0.0',
 'numba==0.53',
 'numpy==1.22.0',
 'openpyxl>=3.0.9,<4.0.0',
 'optuna>=2.10.0,<3.0.0',
 'plotly>=5.5.0,<6.0.0',
 'rouge-score>=0.0.4,<0.0.5',
 'scikit-learn>=1.0.2,<2.0.0',
 'scikit-surprise>=1.1.1,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'sentence-transformers>=2.1.0,<3.0.0',
 'statsmodels>=0.13.1,<0.14.0',
 'torch==1.10.1',
 'torchaudio==0.10.1',
 'torchvision==0.11.2',
 'transformers>=4.15.0,<5.0.0',
 'xgboost>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'ml-init',
    'version': '0.6.0',
    'description': 'Install the main ML libraries',
    'long_description': '# ML Init\n\nML Init is an open package to start your Machine Learning developing project. ML init install the main libraries in the Machine Learning/Deep Learning evironment.\n',
    'author': 'Alberto Rubiales',
    'author_email': 'al.rubiales.b@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<=3.11',
}


setup(**setup_kwargs)
