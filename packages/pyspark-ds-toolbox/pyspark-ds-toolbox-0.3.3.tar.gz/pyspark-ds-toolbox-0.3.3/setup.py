# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspark_ds_toolbox',
 'pyspark_ds_toolbox.causal_inference',
 'pyspark_ds_toolbox.ml',
 'pyspark_ds_toolbox.ml.classification',
 'pyspark_ds_toolbox.ml.data_prep',
 'pyspark_ds_toolbox.ml.feature_importance',
 'pyspark_ds_toolbox.stats',
 'pyspark_ds_toolbox.wrangling']

package_data = \
{'': ['*']}

install_requires = \
['h2o>=3.34.0,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'mlflow>=1.22.0,<2.0.0',
 'numpy==1.21.0',
 'pandas>=1.3.4,<2.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'pyspark>=3.2',
 'seaborn>=0.11.2,<0.12.0',
 'tqdm>=4.62.3,<5.0.0',
 'typeguard>=2.13.2,<3.0.0']

setup_kwargs = {
    'name': 'pyspark-ds-toolbox',
    'version': '0.3.3',
    'description': 'A Pyspark companion for data science tasks.',
    'long_description': '# Pyspark DS Toolbox\n\n<!-- badges: start -->\n[![Lifecycle:\nexperimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pyspark-ds-toolbox.svg)](https://pypi.org/project/pyspark-ds-toolbox/)\n[![CodeFactor](https://www.codefactor.io/repository/github/viniciusmsousa/pyspark-ds-toolbox/badge)](https://www.codefactor.io/repository/github/viniciusmsousa/pyspark-ds-toolbox)\n[![Maintainability](https://api.codeclimate.com/v1/badges/9a85a662305167c5aba1/maintainability)](https://codeclimate.com/github/viniciusmsousa/pyspark-ds-toolbox/maintainability)\n[![Codecov test coverage](https://codecov.io/gh/viniciusmsousa/pyspark-ds-toolbox/branch/main/graph/badge.svg)](https://codecov.io/gh/viniciusmsousa/pyspark-ds-toolbox?branch=main)\n[![Package Tests](https://github.com/viniciusmsousa/pyspark-ds-toolbox/actions/workflows/package-tests.yml/badge.svg)](https://github.com/viniciusmsousa/pyspark-ds-toolbox/actions)\n[![Downloads](https://pepy.tech/badge/pyspark-ds-toolbox)](https://pepy.tech/project/pyspark-ds-toolbox)\n<!-- badges: end -->\n\n\nThe objective of the package is to provide a set of tools that helps the daily work of data science with spark. The documentation can be found [here](https://viniciusmsousa.github.io/pyspark-ds-toolbox/index.html). Feel free to contribute :)\n\n\n## Installation\n\nDirectly from PyPi:\n```\npip install pyspark-ds-toolbox\n```\n\nor from github, note that installing from github will install the latest development version:\n```\npip install git+https://github.com/viniciusmsousa/pyspark-ds-toolbox.git\n```\n\n## Organization\n\nThe package is currently organized in a structure based on the nature of the task, such as data wrangling, model/prediction evaluation, and so on.\n\n```\npyspark_ds_toolbox         # Main Package\n├─ causal_inference           # Sub-package dedicated to Causal Inferece\n│  ├─ diff_in_diff.py   \n│  └─ ps_matching.py    \n├─ ml                         # Sub-package dedicated to ML\n│  ├─ data_prep                  # Sub-package to ML data preparation tools\n│  │  ├─ class_weights.py     \n│  │  └─ features_vector.py \n│  ├─ classification             # Sub-package decidated to classification tasks\n│  │  ├─ eval.py\n│  │  └─ baseline_classifiers.py \n│  └─ feature_importance         # Sub-package with feature importance tools\n│     ├─ native_spark.py\n│     └─ shap_values.py    \n├─ wrangling                  # Sub-package decidated to data wrangling tasks\n│  ├─ reshape.py               \n│  └─ data_quality.py         \n└─ stats                      # Sub-package dedicated to basic statistic functionalities\n   └─ association.py    \n```\n\n',
    'author': 'vinicius.sousa',
    'author_email': 'vinisousa04@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/viniciusmsousa/pyspark-ds-toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
