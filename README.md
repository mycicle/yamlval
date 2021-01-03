# yamlval
Python tool used to easily define a schema for a yaml file. Yamlval allows users to define types for yaml fields and will throw clear and will generate clear and transparent logs for debugging

## If you're skimming this then read these next few points to save yourself a lot of headache
    - Do not use enums in yDict, it will not work, you will get an error
    - Do not use mutliple enums in yList, just make one large enum or you will get an error
    - yAny is true for everything EXCEPT None
    - yNone is true for ONLY None
    - yDict takes tuples of yObjects as inputs, i.e 
    ```
    yDict( (yKeyType, yValueType1, yValueType2, ...), (yKeyType, yValueType1, yValueType2, ...), ...  )
    ```
    Happy Validating!

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

## Longer Example
- This is an example of a .yml or .yaml file which does not match the config,. The structure is mostly there, but I have simulated common errors which are easy to overlook. You can copy-paste and directly run this code to get a feel for the errors thrown by the system. 
- Notice that most validation errors are logged before an exception is raised, letting you see a large number of validation errors simultaneously, saving you important time. 


- Directory structure for example:
```
./
    example.py
    example.yml
```
- Requirements for example:
    - python >= 3.6
    - yamlval
    
```yaml
name: "Michaell"
age: 21
height: "5'11 3/4extrachars"
listOlists: 
  - - - "hello"
      - "sdf"
      - "asdf"
      - "asdf"
    - - "asdfasdf"
      - "asdfasdf"
      - 1.
      - "asdfasdf"
  - - - "hello"
      - "sdf"
      - "asdf"
      - "asdf"
    - - "asdfasdf"
      - "asdfasdf"
      - 1
      - "asdfasdf"
normalList:
  - "hellothere"
  - 4
floatingPoint: 9.
dictOstuff:
  Michael: 
    "string1" : "string2"
  1: 
    - - "string123"
      - "asdf"
      - "asdf"
    - - "asdfasdfasdf"
      - "asdfasdfadsf"
  somewords: "some more words"

anyDict: 
  asdf: 5
  6: "eight"
  NULL: NULL

noneDict:
  asdf: NULL
  5.5: NULL
  5: NULL

anyList: 
  - "asdf"
  - 5
  - 5.5
  - NULL

noneList:
  - NULL
  - NULL
  - NULL

noneListPlus:
  - NULL
  - 5.5
  - 5
  - NULL
  - "string from yamlval here"
```

```python
from yamlval import yString, yList, yEnum, yDict, yInt, yFloat, ySchema, yAny, yNone

from enum import Enum

class Names(Enum):
    mike = "Michael"

class Schema(ySchema):
    name = yEnum(Names)
    age = yInt(lower=0, upper=120)
    height = yString(lower=3, upper=8)
    listOlists = yList(yList(yList(yString(), yInt())), yInt(), lower=2)
    normalList = yList(yString(lower=2), yInt(upper=10))
    floatingPoint = yFloat(upper=10)
    dictOstuff = yDict(
        (yString(), yInt(), yDict((yString(), yString()))),
        (yInt(upper=2), yList(yList(yString(upper=7), upper=2))),
        (yString(), yString()),
    )
    anyDict = yDict(
        (yAny(), yInt(), yString())
    )
    noneDict = yDict(
        (yAny(), yNone())
    )
    anyList = yList(yAny())
    noneList = yList(yNone())
    noneListPlus = yList(yNone(), yFloat())
    
with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
```

If you find any errors, bugs, or simply want to contribute, let me know at mjm.digregorio@gmail.com !

You can also initiate a pull request!

- Mike

Happy Validating!