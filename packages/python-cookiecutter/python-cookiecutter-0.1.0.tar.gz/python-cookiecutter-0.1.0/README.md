# Hypermodern Python Guide

[![Tests](https://github.com/udeepam/python-cookiecutter/workflows/Tests/badge.svg)](https://github.com/udeepam/python-cookiecutter/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/udeepam/python-cookiecutter/branch/master/graph/badge.svg)](https://codecov.io/gh/udeepam/python-cookiecutter)
[![PyPI](https://img.shields.io/pypi/v/python-cookiecutter.svg)](https://pypi.org/project/python-cookiecutter/)

This repository follows the series of articles for [hypermodern python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/).

What is used:
* Package, dependency, and environment manager: `conda`
* Package and dependency manager: `poetry`
* Package manager: `pip`
* Continuous integration: `GitHub Actions`
* Command-line interface: `click`
* Managing git hooks: `pre-commit`
* Data validation: `desert`, `marshmallow`
* Testing:
  * Unit testing: `pytest`
  * Test automation: `nox`
  * Security audit: `Safety`
  * Code coverage: `Coverage.py`
  * Coverage reporting: `codecov`
* Documentation:
  * Check documentation examples: `xdoctest`
  * Documentation: `sphinx`
  * Generate API documentation: `autodoc`, `napoleon`, `sphinx-autodoc-typehints`
* Linting:
  * `flake8`:
    * `flake8-black`: generates warnings if it detects Black would reformat a source file.
    * `flake8-import-order`: generates warnings if import statements are not grouped and ordered in a consistent and PEP 8-compliant way.
    * `flake8-bugbear`: helps you find various bugs and design problems in your programs.
    * `flake8-bandit`: find common security issues in Python code.
    * `flake8-annotations`: detects the absence of type annotations for functions, helping you keep track of unannotated code.
    * `flake8-docstrings`: uses the tool pydocstyle to check that docstrings are compliant with the style recommendations of PEP 257.
  * `mypy`: static type checking.
  * `pytype`: static type checking.
  * `typeguard`: runtime type checking.
  * `darglint`: checks that docstring descriptions match function definitions.
* Formatting:
  * `black`: modifies conflicting files.

## Instructions not in the articles.
1. Clone the repository.
2. Create a new conda environment:
   ```bash
   conda env create -f environment.yml
   ```
3. Download `Coverage.py` using `zsh` cli:
   ```bash
   poetry add --dev 'coverage[toml]' pytest-cov
   ```
