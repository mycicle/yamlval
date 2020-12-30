import yaml

from abc import ABCMeta
from io import TextIOWrapper

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
        logger.info(fields)
        for field in fields:
            logger.info(raw_vars[field])
            logger.info(type(raw_vars[field]))
        return {"this":"that"}

    @classmethod
    def validate_and_load(cls, yamlfile: Optional[TextIOWrapper]) -> Dict[str, Any]: 
        if not isinstance(yamlfile, TextIOWrapper):
            logger.error(f"Your IO obejct is not a StringIO object, type {type(yamlfile)} is unsupported")
        if yamlfile is None:
            logger.error("StringIO object is empty, make sure that your filepath is correct and the file is populated")

        raw_config: Optional[Dict[str, Any]] = yaml.load(yamlfile)

        if raw_config is None:
            logger.error("Unable to read yaml information from the input file, validate that you are using proper yaml syntax")
        
        validated_config: Dict[str, Any] = cls._validate(raw_config)

        return validated_config
            