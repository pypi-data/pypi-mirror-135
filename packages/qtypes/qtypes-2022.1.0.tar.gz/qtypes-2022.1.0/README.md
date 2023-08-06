# qtypes

[![PyPI](https://img.shields.io/pypi/v/qtypes)](https://pypi.org/project/qtypes)
[![Conda](https://img.shields.io/conda/vn/conda-forge/qtypes)](https://anaconda.org/conda-forge/qtypes)
[![black](https://img.shields.io/badge/code--style-black-black)](https://black.readthedocs.io/)
[![log](https://img.shields.io/badge/change-log-informational)](https://gitlab.com/yaq/qtypes/-/blob/main/CHANGELOG.md)

Build qt graphical user interfaces out of simple type objects.

## Installation

TODO

## Types

### Bool

```
value: bool
```

### Button

```
value: None
background_color: str
text: str
text_color: str
```

### Enum
```
value: str
allowed: List[str]
```

### Float

```
value: double
units: str
minimum: double
maximum: double
decimals: int
```

Note that units support works via [pint](https://pint.readthedocs.io)

### Integer

```
value: int
minimum: int
maximum: int
```

### String

```
value: str
```

## Examples

`qtypes` comes with a few examples right out of the box.
Run them using the python module syntax, e.g.:

```bash
$ python -m qtypes.examples one_of_each
```

Included examples:

| example       | description                                                            |
| ------------- | ---------------------------------------------------------------------- |
| `one_of_each` | Simple example displaying one of each type with some inspection tools. |
| `units`       | Example demonstrating units support for qtypes Float object.           |
