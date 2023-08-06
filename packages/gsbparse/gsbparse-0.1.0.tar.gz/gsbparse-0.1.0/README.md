# gsbparse

A Python parser for [Grisbi](https://github.com/grisbi/grisbi)'s `.gsb` files.

## User Quickstart

`gsbparse` provides two main classes for easily using content of a [Grisbi](https://github.com/grisbi/grisbi)'s `.gsb` file in Python: `gsbparse.AccountFile` and `gsbparse.Transactions`.
Both classes are instantiated with a pointer to a `.gsb` file: either filepath (`str`) or a file object itself.

### Installation

You can install `gsbparse` from PyPI:

```shell
pip install gsbparse
```

### How to use

```python
from gsbparse import AccountFile

AccountFile("path/to/my_account_file.gsb")
```

## Development Quickstart

This project adheres to [Semantic Versioning](https://semver.org/), and releases descriptions can be found in `CHANGELOG.md`.

### Use your own environment management preference

For `pyvenv`:

```shell
python -m venv .venv/
source .venv/bin/activate
```

### Install this package

```shell
git clone git@github.com:EBoisseauSierra/gsbparse.git
cd gsbparse
pip install --upgrade pip
pip install -e '.[dev,test]'
```

### Initialise pre-commit hooks

The [pre-commit hooks](https://pre-commit.com) defined in this repo ensure that code formating and linting is applied on any piece of code committed. This should enable a cleaner code base and less “formatting noise” in commits.

To install the hooks, simply run:

```shell
pre-commit install
```

### Contributing

1. Fork this repo (<https://github.com/EBoisseauSierra/gsbparse/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
