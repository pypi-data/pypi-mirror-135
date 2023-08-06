# pycltools package documentation

[![GitHub license](https://img.shields.io/github/license/a-slide/pycltools.svg)](https://github.com/a-slide/pycltools/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/pycltools.svg)](https://badge.fury.io/py/pycltools)
[![Upload Python Package](https://github.com/a-slide/pycltools/actions/workflows/python-publish.yml/badge.svg)](https://github.com/a-slide/pycltools/actions/workflows/python-publish.yml)
---

**pycltools is a package written in python3 containing a collection of generic functions and classes for file parsing, manipulation...**

---

pycltools contains many functions organized in several categories:

* jupyter notebook specific tools
* file predicates
* path manipulation
* string formatting
* file manipulation
* file information/parsing
* directory manipulation
* shell manipulation
* dictionnary formatting
* table formatting
* web tools
* functions tools
* ssh tools

Many of the function replicate bash commands in pure python 3.

Please be aware that pycltools is an experimental package that is still under development. It was tested under Linux Ubuntu 16.04 and in an HPC environment running under Red Hat Enterprise 7.1. You are welcome to raise issues, contribute to the development and submit patches or updates

## Installation

Ideally, before installation, create a clean python3 virtual environment to deploy the package, using virtualenvwrapper for example (see http://www.simononsoftware.com/virtualenv-tutorial-part-2/).

### Option 1: Direct installation with pip from pypi or github

Install or upgrade the package with pip from pypi

```python
pip3 install pycltools --upgrade
```

Or from github to get the last version

```python
pip3 install git+https://github.com/a-slide/pycltools.git --upgrade
```

### Option 2: Clone the repository and install locally in develop mode

With this option, the package will be locally installed in “editable” or “develop” mode. This allows the package to be both installed and editable in project form. This is the recommended option if you wish to participate to the development of the package. As for the option before, the required dependencies will be automatically installed.

```python
git clone https://github.com/a-slide/pycltools.git
cd pycltools
chmod u+x setup.py
pip3 install -e ./
```

### Option 3: Local installation without pip

This option is also suitable if you are interested in further developing the package, but requires a little bit more hands-on.

* Clone the repository locally

```python
git clone https://github.com/a-slide/pycltools.git
```

* Add the package directory (./pycltools/pycltools) to you python3 PATH (depending on you OS and whether you want it to be permanent ot not)

## Usage

List of all functions contained in the package with a short description: [functions list Notebook](https://a-slide.github.io/pycltools/pycltools_functions_list.html)

Detailed usage of most of the functions with basic tests: [Tests Notebook](https://a-slide.github.io/pycltools/pycltools_tests.html)

## Authors and Contact

Adrien Leger - 2019

EMBL EBI

* <aleg@ebi.ac.uk>
* [Github](https://github.com/a-slide)
