from abc import ABC, abstractmethod
from typing import Union
from featurestorebundle.entity.Entity import Entity


class FeaturesReaderInterface(ABC):
    @abstractmethod
    def read(self, entity: Union[Entity, str]):
        pass

    @abstractmethod
    def read_safe(self, entity: Entity):
        pass

    @abstractmethod
    def exists(self, entity: Union[Entity, str]):
        pass
