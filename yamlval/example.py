import yaml

from enum import Enum
from schema.yEnum import yEnum
from schema.yInt import yInt
from schema.yFloat import yFloat
from schema.yString import yString
from schema.ySchema import ySchema
from schema.yList import yList
class Names(Enum):
    mike = "Michael"

class Schema(ySchema):
    name = yEnum(Names)
    age = yInt(lower=0, upper=120)
    height = yString(lower=3, upper=8)
    listOlists = yList(yList(yList(yString(), yInt())), yInt(), lower=2)
    normalList = yList(yString(lower=2), yInt(upper=10))
    floatingPoint = yFloat(upper=10)
    
with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
