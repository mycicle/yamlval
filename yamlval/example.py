import yaml
from schema.YValSchema import YValSchema

class Schema(YValSchema):
    field1 = "Hello"
    field2 = 1
    yoho = "yoo hoo!"

config = {}
with open("example.yml") as f:
    config = Schema.validate_and_load(f)

print(config)
