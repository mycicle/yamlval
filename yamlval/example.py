import yaml

from enum import Enum
from schema.yEnum import yEnum
from schema.yInt import yInt
from schema.yString import yString
from schema.ySchema import ySchema

class Names(Enum):
    mike = "Michel"

class Schema(ySchema):
    name = yEnum(Names)
    age = yInt(lower=0, upper=120)
    height = yString(lower=3, upper=8)

with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
