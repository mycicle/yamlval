def main():
    import yaml

    from enum import Enum
    from yamlval.yEnum import yEnum
    from yamlval.yInt import yInt
    from yamlval.yFloat import yFloat
    from yamlval.yString import yString
    from yamlval.ySchema import ySchema
    from yamlval.yList import yList
    from yamlval.yDict import yDict
    from yamlval.yAny import yAny
    from yamlval.yNone import yNone
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

if __name__ == "__main__":
    main()
