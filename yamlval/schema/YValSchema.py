import yaml

from abc import ABCMeta
from io import TextIOWrapper
from .yEnum import yEnum
from .yList import yList
from loguru import logger

from typing import Dict, Any, Optional

class YValSchema(metaclass=ABCMeta): 
    """
    Base class for yval schemas
    Fields cannot start with a double underscore, "__", or "_abc" otherwise they will not be recognized by the 
    typing validator
    """
    def __init__(self):
        pass

    @classmethod
    def _validate(cls, raw_config: Dict[str, Any]) -> Dict[str, Any]:
        raw_vars = vars(cls)
        fields = [var for var in list(raw_vars.keys()) if not callable(getattr(cls, var)) and not var.startswith("__") and not var.startswith("_abc")]
        config_fields = [field for field in raw_config.keys()]
        for field in config_fields:
            if field not in fields:
                raise ValueError(f"field <{field}> is defined in the config, but is not properly defnied within schema <{cls.__name__}>. Make sure to use type classes from yval!")

        for field in fields:
            if field not in raw_config:
                if not isinstance(raw_vars[field], yEnum):
                    raise TypeError(f"field <{field}> is not defined in config file and {cls.__name__}[{field}] is not a yEnum which accepts 'None' as an input")
                if not raw_vars[field].matches(None):
                    raise ValueError(f"field <{field}> is not defined in config file and {cls.__name__}[{field}] is a yEnum, but it does not accept 'None' as an input\nexpected \
                                        {[var for var in raw_vars[field].get_values()]}")

            if not raw_vars[field].matches(raw_config[field]):
                raise TypeError(
                        f"In field <{field}> expected valid:\n<{[var for var in raw_vars[field].get_values()] if isinstance(raw_vars[field], yEnum) else [typ for typ in raw_vars[field].types] if isinstance(raw_vars[field], yList) else type(raw_vars[field])}>\naccording to schema <{cls.__name__}>")

        return raw_config

    @classmethod
    def validate_and_load(cls, yamlfile: Optional[TextIOWrapper], Loader: Any = yaml.FullLoader) -> Dict[str, Any]: 
        if not isinstance(yamlfile, TextIOWrapper):
            logger.error(f"Your IO obejct is not a StringIO object, type {type(yamlfile)} is unsupported")
        if yamlfile is None:
            logger.error("StringIO object is empty, make sure that your filepath is correct and the file is populated")

        # yaml.FullLoader is unsafe. This can be replaced via function argument to an alternative loader
        # see https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation for more details
        raw_config: Optional[Dict[str, Any]] = yaml.load(yamlfile, Loader=Loader)

        if raw_config is None:
            logger.error("Unable to read yaml information from the input file, validate that you are using proper yaml syntax")
        
        validated_config: Dict[str, Any] = cls._validate(raw_config)

        return validated_config
            