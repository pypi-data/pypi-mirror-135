# Polysynth Python SDK

The official Python client for [Polysynth](https://polysynth.com/).

Documentation is available [here](https://docs.polysynth.com/developer-resources/python-sdk).

## Getting Started
This library attempts to present a clean interface to Polysynth, but in order to use it to its full potential, you must familiarize yourself with the official Polysynth documentation:
- Installation
- Quoting Prices
- Making Trades
- Managing Collaterals
- Ratios

### Installation
You can install the latest release from PyPI, or install the latest commit directly from git:
- Install the latest release from PyPI:
 ``` pip install polysynth```

- Install from git:
 ``` pip install git+https://github.com/kryptolabs/polysynth-python.git```

- Clone and install with poetry:
```
git clone https://github.com/kryptolabs/polysynth-python.git
cd polysynth-python
poetry install
```
### Quoting Prices
##### input_price
Returns the amount of ETH you get for 1 USDP
```
client.input_price("ETH-USDC", "BUY", 1)
```
##### output_price
Returns the amount of USDP you need to pay to get 1000 ETH
```
client.output_price(ETH-USDC, “BUY”, 1000)
```

### Making Trades
##### open_position
Open a long position against 1000 USDP worth ETH with a leverage of 1x and slippage  tolerance of 0%
 ```
client.open_position(ETH-USDC, “BUY”, 1000, 1, 0)
```
##### close_position
Closes a trader’s all positions for ETH with zero slippage tolerance
```
client.close_position(ETH-USDC, 0)
```

### Managing Collaterals
##### add_collateral
Add 1000 USDP worth collateral in ETH AMM
```
client.add_collateral(ETH-USDC, 1000)
```

##### remove_collateral
Remove 500 USDP worth collateral from ETH AMM
```
client.remove_collateral(ETH-USDC, 500)
```

### Ratios
##### fluctuation_limit_ratio
Get fluctuation limit ratio of ETH market
```
client.fluctuation_limit_ratio(ETH-USDC)
```

##### trade_limit_ratio
Get trade limit ratio of ETH market
```
client.trade_limit_ratio(ETH-USDC)
```

##### collateral_ratio
Get collateral ratio of ETH market
```
client.collateral_ratio(“ETH-USDC”)
```

##### fee_ratio
Get fee ratio of the platform
```
client.fee_ratio()
```

##### init_collateral_ratio
Get initial collateral ratio of the platform
```
client.init_collateral_ratio()
```

##### liquidation_fee_ratio
Get liquidation fee ratio of the platform
```
client.liquidation_fee_ratio()
```

##### maintenance_collateral_ratio
Get maintenance collateral ratio of the platform
```
client.maintenance_collateral_ratio()
```

##### partial_liquidation_ratio
Get partial liquidation ratio of the platform
```
client.partial_liquidation_ratio()
```


### Testing
To run the full test suite, in the project directory set the `PROVIDER` env variable to a  provider, and run:

```
poetry install
export PROVIDER= # URL of provider, e.g. https://mainnet.infura.io/v3/...
poetry shell
poetry run pytest
```

### Publish to pip
To build and publish the package to pip,run:

```
poetry shell
poetry build
poetry publish
```

## Authors
* [Arpit Singh](https://github.com/gyan/)
* [Paritosh Gupta](https://github.com/mavvverick)