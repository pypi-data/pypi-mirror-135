# Gregorian Months

Conduct with the Gregorian calendar months

## Usage

Get each month number by its name:

```python
from gregorian_months import get_number


get_number("July") # Will return `7`
get_number("January") # Will return `1`
get_number("October") # Will return `10`
```

The package supports all cases:

```python
from gregorian_months import get_number


get_number("july") # Will return `7`
get_number("JANUARY") # Will return `1`
get_number("OcToBer") # Will return `10`
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package:

```bash
pip install gregorian-months
```
