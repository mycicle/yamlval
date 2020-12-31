import yaml
from enum import Enum
from schema.YValSchema import YValSchema
from schema.yEnum import yEnum
class Ticker(Enum):
    aapl = "AAPL"
    msft = "MSFT"
    tsla = "TSLA"
    nothing = None
class Schema(YValSchema):
    field1 = str
    field2 = int
    yoho = str
    ticker = yEnum(Ticker)

config = {}
with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
