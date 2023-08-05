# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py2dmat', 'py2dmat.algorithm', 'py2dmat.solver', 'py2dmat.util']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14,<2.0', 'tomli>=1,<2']

extras_require = \
{'all': ['scipy>=1,<2', 'mpi4py>=3,<4', 'physbo>=1.0.0'],
 'bayes': ['physbo>=1.0.0'],
 'exchange': ['mpi4py>=3,<4'],
 'min_search': ['scipy>=1,<2']}

entry_points = \
{'console_scripts': ['py2dmat = py2dmat:main',
                     'py2dmat_neighborlist = py2dmat.util.neighborlist:main']}

setup_kwargs = {
    'name': 'py2dmat',
    'version': '2.0.0',
    'description': 'Data-analysis software of quantum beam diffraction experiments for 2D material structure',
    'long_description': '# 2DMAT -- Data-analysis software of quantum beam diffraction experiments for 2D material structure\n\n2DMAT is a framework for applying a search algorithm to a direct problem solver to find the optimal solution.\nAs the standard direct problem solver, the experimental data analysis software for two-dimensional material structure analysis is prepared.\nThe direct problem solver gives the deviation between the experimental data and the calculated data obtained under the given parameters such as atomic positions as a loss function used in the inverse problem.\nThe optimal parameters are estimated by minimizing the loss function using a search algorithm. For further use, the original direct problem solver or the search algorithm can be defined by users.\nIn the current version, for solving a direct problem, 2DMAT offers the wrapper of the solver for the total-reflection high-energy positron diffraction (TRHEPD) experiment.\nAs algorithms, it offers the Nelder-Mead method, the grid search method, the Bayesian optimization method, and the replica exchange Monte Carlo method. In the future, we plan to add other direct problem solvers and search algorithms in 2DMAT.\n\n| Branch |                Build status                 |                                       Documentation                                       |\n| :----: | :-----------------------------------------: | :---------------------------------------------------------------------------------------: |\n| [master][source/master] (latest) | [![master][ci/master/badge]][ci/master/uri] |        [![doc_en][doc/en/badge]][doc/en/uri] [![doc_ja][doc/ja/badge]][doc/ja/uri]        |\n| [v2.0.0][source/stable] (latest stable) |                     --                      | [![doc_en][doc/en/badge]][doc/stable/en/uri] [![doc_ja][doc/ja/badge]][doc/stable/ja/uri] |\n\n## py2dmat\n\n`py2dmat` is a python framework library for solving inverse problems.\nIt also offers a driver script to solve the problem with predefined optimization algorithms\nand direct problem solvers (`py2dmat` also means this script).\n\n### Prerequists\n\n- Required\n  - python >= 3.6\n  - numpy >= 1.14\n  - tomli >= 1.0.0\n- Optional\n  - scipy\n    - for `minsearch` algorithm\n  - mpi4py\n    - for `exchange` algorithm\n  - physbo >= 1.0\n    - for `bayes` algorithm\n\n### Install\n\n- From PyPI (Recommended)\n  - `python3 -m pip install -U py2dmat`\n    - If you want to install pre-release version (e.g., v2.0-beta), use `--pre` option like `python3 -m pip install -U --pre`\n    - If you install them locally, use `--user` option like `python3 -m pip install -U --user`\n    - [`pipx`](https://pipxproject.github.io/pipx/) may help you from the dependency hell :p\n- From Source (For developers)\n  1. update `pip >= 19` by `python3 -m pip install -U pip`\n  1. `python3 -m pip install 2DMAT_ROOT_DIRECTORY` to install `py2dmat` package and `py2dmat` command\n\n### Simple Usage\n\n- `py2dmat input.toml` (use the installed script)\n- `python3 src/py2dmat_main.py input.toml` (use the raw script)\n- For details of the input file, see the document.\n\n## License\n\nThis package is distributed under GNU General Public License version 3 (GPL v3) or later.\n\n## Copyright\n\n© *2020- The University of Tokyo. All rights reserved.*\nThis software was developed with the support of "*Project for advancement of software usability in materials science*" of The Institute for Solid State Physics, The University of Tokyo.\n\n[source/master]: https://github.com/issp-center-dev/2DMAT/\n[source/stable]: https://github.com/issp-center-dev/2DMAT/tree/v2.0.0\n[ci/master/badge]: https://github.com/issp-center-dev/2DMAT/workflows/Test/badge.svg?branch=master\n[ci/master/uri]: https://github.com/issp-center-dev/2DMAT/actions?query=branch%3Amaster\n[doc/en/badge]: https://img.shields.io/badge/doc-English-blue.svg\n[doc/en/uri]: https://issp-center-dev.github.io/2DMAT/manual/master/en/index.html\n[doc/ja/badge]: https://img.shields.io/badge/doc-Japanese-blue.svg\n[doc/ja/uri]: https://issp-center-dev.github.io/2DMAT/manual/master/ja/index.html\n[doc/stable/en/uri]: https://issp-center-dev.github.io/2DMAT/manual/v2.0.0/en/index.html\n[doc/stable/ja/uri]: https://issp-center-dev.github.io/2DMAT/manual/v2.0.0/ja/index.html\n',
    'author': '2DMAT developers',
    'author_email': '2dmat-dev@issp.u-tokyo.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/issp-center-dev/2DMAT',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
