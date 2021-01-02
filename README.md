# yamlval
Python tool used to easily define a schema for a yaml file. Yamlval allows users to define types for yaml fields and will throw clear and will generate clear and transparent logs for debugging

## Example
```yaml
ticker: "AAPL"
fields: 
  - "Close"
  - "Adj Close"
  - "Open"
col_map: 
  2 : "hello"
  3 : "hello plus one"
transform: 
  - lag: 1
  - scalar: 2
  - targets: 
      - "col1"
      - "col2"
      - "col3"
```

```python
from yamlval import yString, yList, yEnum, yDict, yInt, yFloat, ySchema

from enum import Enum

class Ticker(Enum):
    msft = "MSFT"
    aapl = "AAPL"
    spy = "^GSPC"

class ValuationFields(Enum):
    close = "Close"
    adjclose = "Adj Close"
    opn = "Open"

class Schema(ySchema):
    ticker = yEnum(Ticker)
    fields = yList(yEnum(ValuationFields))
    col_map = yDict(
            (yInt(), yString())
        )
    transform = yList(
                    yDict(
                        (yString(), yInt(), yList(yString(), lower=3, upper=3))
                    )
                )

config = []
with open("example.yml", "r") as f:
    config = Schema.validate_and_load(f)
print(config) 
```