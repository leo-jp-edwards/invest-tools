# invest-tools

[![PyPI version](https://badge.fury.io/py/invest-tools.svg)](https://badge.fury.io/py/invest-tools)
[![codecov](https://codecov.io/gh/leo-jp-edwards/invest-tools/graph/badge.svg?token=C1W8MZFS80)](https://codecov.io/gh/leo-jp-edwards/invest-tools)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Tools to manage portfolio risk analysis**

## Installation

As a python package this should be installable through:

> `pip install invest-tools`

Or:

> `poetry add invest-tools`

### Dependencies

The dependencies of this project can be seen in the `pyproject.toml` file. However for completeness there is a dependcy on `pandas`, `statsmodels` and `matplotlib` as the basics.

## Data Inputs

There are three data inputs which should be present for the package to work as expected. 

The path strings to the csvs can be passed in. 

1. Portfolio price data as a CSV

| TIDM | Date | Open | High | Low | Close | Volume | Adjustment |
|------|------|------|------|-----|-------|--------|------------|
| EG | 01/01/2023 | 1 | 1 | 1 | 1 | 1 | 1 |
| EG2 | 01/01/2023 | 1 | 1 | 1 | 1 | 1 | 1 |

2. Currency data as a CSV

| Date | Open | High | Low | Close | Adj Close | Volume |
|------|------|------|-----|-------|-----------|--------|
| 01/01/2023 | 1 | 1 | 1 | 1 | 1 | 1 |

3. Fama French Data as a CSV

This can be found [here](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)

## Example

Build a portfolio of two securities called `EG` and `EG2` with the weighting split 50:50 between the two. One is denominated in GBP and one in USD.

This will output the mean returns of such a portfolio.

```python
import numpy as np
from invest_tools import portfolio

portfolio_definition = {
    "EG": {
        "weight": 0.5,
        "currency": "gbp"
    },
    "EG2": {
        "weight": 0.5,
        "currency": "usd"
    }
}

port = portfolio.Portfolio(portfolio_definition, portfolio.Currency.GBP)
port.get_usd_converter("path/to/csv")
port.get_prices("path/to/csv")
port.build()
print(np.mean(port.backtest.portfolio_returns))
```

## Roadmap

- [ ] Add an input validator
- [ ] Add logging
- [ ] Add deeper analysis methods
    - [ ] Coppock Curve
    - [ ] Fama French
    - [ ] Excess Returns
    - [ ] Maximum Drawdown
    - [ ] Calculate Moments
- [ ] Add further testing
- [ ] Make the package more generic

## License

[MIT](LICENSE)

## Contact

Just open an issue I guess?