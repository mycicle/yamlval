import yaml
from enum import Enum
from schema.YValSchema import YValSchema
from schema.yEnum import yEnum
from schema.yString import yString
from schema.yInt import yInt
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

config = {}
with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
