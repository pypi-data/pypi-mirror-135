# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xicorpy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0',
 'pandas>=1.2,<2.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7,<2.0']

extras_require = \
{':extra == "typings"': ['mypy==0.931'],
 'docs': ['mkdocstrings>=0.17,<0.18', 'mkdocs-material>=8.1,<8.2']}

setup_kwargs = {
    'name': 'xicorpy',
    'version': '0.1.2',
    'description': "Python implementation of Chatterjee's Rank Correlation, its modifications, and other offshoots",
    'long_description': '# Chatterjee\'s Xi, its Applications, and Offshoots\n\nXicorPy is a Python package implementing **Chatterjee\'s Xi**, and its various offshoots. You can use the package with raw python objects, NumPy arrays, or Pandas DataFrames.\n\nPlease see the [Documentation][docs] for an introductory tutorial and a full\nuser guide.\n\n## Features\n\nThe package currently implements:   \n\n1. Chatterjee\'s Xi from [1]\n2. Modified Xi from [2]\n3. Codependence Coefficient from [3]\n4. Feature Ordering by Conditional Independence (FOCI) for Feature Selection from [3]\n\n\n## Usage\n\nThe package is available on PyPI. You can install using pip: `pip install xicorpy`.\n\n\n```python\nimport xicorpy\n\nx = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]\ny = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]\nxi = xicorpy.compute_xi_correlation(x, y)\n\nxi, p_value = xicorpy.compute_xi_correlation(x, y, get_p_values=True)\n\n```\n\nRefer to the [Docs][docs] for more details.\n\n## Contributing to XiCorPy\n\nAny help with the package is greatly appreciated! Pull requests and bug reports are greatly welcome!\n\n\n## Citations:\n\n1. [Chatterjee (2020). "A new coefficient of correlation"](https://arxiv.org/abs/1909.10140)\n2. [Lin and Han (2021). "On boosting the power of Chatterjee\'s rank correlation"](https://arxiv.org/abs/2108.06828)\n3. [Azadkia and Chatterjee (2021). "A simple measure of conditional dependence"](https://arxiv.org/abs/1910.12327)\n\n<!-- Links -->\n[docs]: https://swarnakumar.github.io/xicorpy/\n',
    'author': 'Swarna Vallabhaneni',
    'author_email': 'swarnakumar@gmail.com',
    'maintainer': 'Swarna Vallabhaneni',
    'maintainer_email': 'swarnakumar@gmail.com',
    'url': 'https://swarnakumar.github.io/xicorpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
