import yaml

from abc import ABCMeta
from io import TextIOWrapper
from loguru import logger
from typing import Dict, Any, Optional

from .yEnum import yEnum

class ySchema(metaclass=ABCMeta):
    def __init__(self):
        pass

    @classmethod
    def _validate(cls, raw_config: Dict[Any, Any]) -> Dict[Any, Any]:
        raw_vars = vars(cls)
        validation_fields = [var for var in list(raw_vars.keys()) if not callable(getattr(cls, var)) and not var.startswith("__") and not var.startswith("_abc")]
        valid: bool = True
        config_fields = [field for field in raw_config.keys()]
        for field in config_fields:
            if field not in validation_fields:
                raise ValueError(f"field <{field}> is defined in the config, but is not properly defnied within schema <{cls.__name__}>. Make sure to use type classes from yval!")
        
        for val_field in validation_fields:
            if val_field not in config_fields:
                if not isinstance(raw_vars[val_field], yEnum):
                    raise TypeError(f"field <{val_field}> is not defined in config file and {cls.__name__}[{val_field}] is not a yEnum which accepts 'None' as an input")
                
                matches, err = raw_vars[val_field].matches(None)
                if not matches:
                    for error in err:
                        logger.error(error)
                    raise ValueError(f"field <{val_field}> is not defined in config file and {cls.__name__}[{val_field}] is a yEnum, but it does not accept 'None' as an input\nexpected \
                                        {[var for var in raw_vars[val_field].get_values()]}")

            matches, err = raw_vars[val_field].matches(raw_config[val_field])
            if not matches:
                valid = False
                logger.error(f"In field <{val_field}> expected valid input as per schema <{cls.__name__}>")
                for error in err:
                    logger.warning(error)

        if not valid:
            raise TypeError(
                    f"Invalid inputs found as per schema <{cls.__name__}>")
        
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