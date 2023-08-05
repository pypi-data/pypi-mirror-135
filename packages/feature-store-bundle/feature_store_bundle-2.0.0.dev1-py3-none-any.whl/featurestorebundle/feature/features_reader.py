from typing import List, Optional
from injecta.container.ContainerInterface import ContainerInterface
from daipecore.function.input_decorator_function import input_decorator_function
from featurestorebundle.feature.FeatureStore import FeatureStore


@input_decorator_function
def read_latest(entity_name: str, feature_names: Optional[List[str]] = None):
    def wrapper(container: ContainerInterface):
        feature_store: FeatureStore = container.get(FeatureStore)

        return feature_store.get_latest(entity_name, feature_names)

    return wrapper
