from typing import Optional
from abc import ABC, abstractmethod


class MetadataReaderInterface(ABC):
    @abstractmethod
    def read(self, entity_name: Optional[str] = None):
        pass
