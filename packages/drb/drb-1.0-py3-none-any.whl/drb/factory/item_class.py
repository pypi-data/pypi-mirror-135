import os
import enum
import uuid
import yaml
import jsonschema
from jsonschema.exceptions import ValidationError
from typing import Optional

from .factory import DrbFactory, FactoryLoader
from .signature import Signature, parse_signature


class ItemClassType(enum.Enum):
    SECURITY = 'SECURITY'
    PROTOCOL = 'PROTOCOL'
    CONTAINER = 'CONTAINER'
    FORMATTING = 'FORMATTING'


class ItemClass:
    """
    Defines a type of item, this type is described in each DRB topic or
    implementation.

    Parameters:
        data (dict): data of item class definition
    Raises:
        KeyError: if data content is not valid
        DrbException: if
    """
    __schema_path = os.path.join(os.path.dirname(__file__), 'it_schema.yml')
    __schema = None

    @classmethod
    def validate(cls, path: str):
        """
        Checks validity of an item class description file.
        Parameters:
            path (str): path of item class description file
        Raises:
            FileNotFoundError - if path does not exist
            ValidationError - if the description file is not valid
        """
        if cls.__schema is None:
            with open(cls.__schema_path) as file:
                cls.__schema = yaml.safe_load(file)

        with open(path) as file:
            for it in yaml.safe_load_all(file):
                jsonschema.validate(it, cls.__schema)

    def __init__(self, data: dict):
        self.__id = uuid.UUID(data['id'])
        self.__label = data['label']
        self.__category = ItemClassType(data['category'])
        self.__signature = parse_signature(data['signature'])
        if 'description' in data:
            self.__description = data['description']
        else:
            self.__description = None
        if 'subClassOf' in data:
            self.__parent = uuid.UUID(data['subClassOf'])
        else:
            self.__parent = None
        if 'factory' in data:
            factory = data['factory']
            self.__factory_name = factory['name']
            if 'classpath' in factory:
                FactoryLoader().load_factory(factory['name'],
                                             factory['classpath'])
        else:
            self.__factory_name = None

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def parent_class_id(self) -> uuid.UUID:
        return self.__parent

    @property
    def label(self) -> str:
        return self.__label

    @property
    def description(self) -> str:
        return self.__description

    @property
    def category(self) -> ItemClassType:
        return self.__category

    @property
    def factory(self) -> Optional[DrbFactory]:
        if self.__factory_name is not None:
            return FactoryLoader().get_factory(self.__factory_name)
        return None

    @property
    def signature(self) -> Signature:
        return self.__signature
