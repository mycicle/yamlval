import yaml
from enum import Enum
from schema.YValSchema import YValSchema
from schema.yEnum import yEnum
from schema.yString import yString
from schema.yInt import yInt
from schema.yFloat import yFloat
from schema.yList import yList
from schema.yAny import yAny
from schema.yDict import yDict
class Ticker(Enum):
    aapl = "AAPL"
    msft = "MSFT"
    tsla = "TSLA"
    nothing = None
class Schema(YValSchema):
    field1 = yString(lower=1, upper=5)
    field2 = yInt(lower=0, upper=100)
    yoho = yString(upper=2)
    ticker = yEnum(Ticker)
    someList = yList(yString(upper=10), yInt(upper=100), yFloat(upper=20.), lower=2, upper=8)
    literally = yAny()
    anything = yAny()
    dicti = yDict(
                (yString(), 
                    yFloat(), yList(yInt(), yEnum(Ticker))), 
                (yInt(), 
                    yString()), 
                upper = 3)
    anyDict = yDict(
                (yAny(), yAny()))

config = {}
with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
