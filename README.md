# yamlval
Python tool used to easily define a schema for a yaml file. Yamlval allows users to define types for yaml fields and will generate clear and transparent logs for debugging.
It's the yaml type validator of your dreams!

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
### You can also call yObject.match() method to validate separately!
- If you do not want to make an entire schema, want to just validate tehe type of an object, or want to validate to a degree above what yamlval can do by default, you can define a yObject and then call the .matches() method separately!

- For example, lets say you have a string = stringToCheck, and you want to check if it's part of an enum, you can define checker = yEnum(EnumName) and then call checker.matches(stringToCheck). This will return a tuple matching the following format:
- Tuple[bool, Optional[List[str]]] = (match, err if not match else None)
- Translation: a tuple with a true/false value for the match at the 0th index, and a list of strings containing the caught errors (if there are any) or 'None' (if there are no errors) at the 1st index.

```python
from yamlval import yEnum

from enum import Enum

class Names(Enum):
    mike = "Michael"

checker = yEnum(Names)
stringToCheck = "Michaelll"
(match, err) = checker.matches(stringToCheck)
if not match:
    print(err)
```

will yield

```
["Input <Michaelll> not in <['Michael']>"]
```

You can also iterate through all validation errors in err and then print them separately to get a nicer looking output for multiple validation errors.

```python 
checker = yEnum(Names)
stringToCheck = "Michaelll"
(match, err) = checker.matches(stringToCheck)
if not match:
    for error in err:
        print(error)
```

This will work for any of the yObject types (yDict, yList, yString, yInt, ...)
and is actually the foundation of the internal implementation of yamlval.

==========================================================================

If you find any errors, bugs, or simply want to contribute, let me know at mjm.digregorio@gmail.com !

You can also initiate a pull request!

\- Mike

Happy Validating!