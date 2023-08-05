from typing import List, Optional
from pyspark.sql import DataFrame
from featurestorebundle.feature.reader.FeaturesReaderInterface import FeaturesReaderInterface
from featurestorebundle.metadata.reader.MetadataReaderInterface import MetadataReaderInterface
from featurestorebundle.delta.feature.DeltaRainbowTableManager import DeltaRainbowTableManager
from featurestorebundle.feature.FeaturesFilteringManager import FeaturesFilteringManager


class FeatureStore:
    def __init__(
        self,
        features_reader: FeaturesReaderInterface,
        metadata_reader: MetadataReaderInterface,
        rainbow_table_manager: DeltaRainbowTableManager,
        features_filtering_manager: FeaturesFilteringManager,
    ):
        self.__features_reader = features_reader
        self.__metadata_reader = metadata_reader
        self.__rainbow_table_manager = rainbow_table_manager
        self.__features_filtering_manager = features_filtering_manager

    def get_latest(self, entity: str, features: Optional[List[str]] = None):
        features = features or []
        feature_store = self.__features_reader.read(entity)
        rainbow_table = self.__rainbow_table_manager.read(entity)

        return self.__features_filtering_manager.get_latest(feature_store, rainbow_table, features)

    def get_for_target(self, entity: str, targets: DataFrame, features: Optional[List[str]] = None, skip_incomplete_rows: bool = False):
        features = features or []
        feature_store = self.__features_reader.read(entity)
        rainbow_table = self.__rainbow_table_manager.read(entity)

        return self.__features_filtering_manager.get_for_target(feature_store, rainbow_table, targets, features, skip_incomplete_rows)

    def get_metadata(self, entity: Optional[str] = None):
        return self.__metadata_reader.read(entity)
