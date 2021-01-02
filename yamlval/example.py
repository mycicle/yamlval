import yaml

from enum import Enum
from schema.yEnum import yEnum
from schema.yInt import yInt
from schema.yFloat import yFloat
from schema.yString import yString
from schema.ySchema import ySchema
from schema.yList import yList
from schema.yDict import yDict
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
    
with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
