from typing import List
from pyspark.sql import functions as f
from pyspark.sql import DataFrame
from pyspark.sql.window import Window
from featurestorebundle.delta.feature.schema import get_rainbow_table_hash_column, get_rainbow_table_features_column


class FeaturesFilteringManager:
    def get_latest(
        self,
        feature_store: DataFrame,
        rainbow_table: DataFrame,
        features: List[str],
    ):
        if not features:
            features = self.get_registered_features(feature_store)

        self.check_features_exist(feature_store, features)

        id_column = feature_store.columns[0]
        time_column = feature_store.columns[1]
        features_hash_column = feature_store.columns[2]
        technical_columns = [id_column, time_column, features_hash_column]

        features_data = feature_store.join(rainbow_table, on=get_rainbow_table_hash_column().name).withColumn(
            "features_intersect", f.array_intersect(get_rainbow_table_features_column().name, f.array(*map(f.lit, features)))
        )

        relevant_features = features_data.select(f.array_distinct(f.flatten(f.collect_set("features_intersect")))).collect()[0][0]
        feature_types = [field.dataType for field in feature_store.schema if field.name not in technical_columns]

        for feature in relevant_features:
            features_data = features_data.withColumn(
                f"{feature}_",
                f.when(f.array_contains(f.col("features_intersect"), feature) & f.col(feature).isNotNull(), f.col(feature)).when(
                    f.array_contains(f.col("features_intersect"), feature) & f.col(feature).isNull(), "<NULL>"
                ),
            )

        window = (
            Window().partitionBy(id_column).orderBy(f.desc(time_column)).rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
        )

        features_data = (
            features_data.select(
                id_column,
                *[f.first(f"{feature}_", ignorenulls=True).over(window).alias(feature) for feature in relevant_features],
                f.array_distinct(f.flatten(f.collect_set("features_intersect").over(window))).alias("computed_features"),
            )
            .filter(f.size("computed_features") == len(relevant_features))
            .groupBy(id_column)
            .agg(*[f.first(feature).alias(feature) for feature in relevant_features])
            .replace("<NULL>", None)
        )

        features_data = features_data.select(
            id_column, *[f.col(feature).cast(type_) for feature, type_ in zip(features, feature_types) if feature in relevant_features]
        )

        return features_data

    def get_for_target(
        self,
        feature_store: DataFrame,
        rainbow_table: DataFrame,
        targets: DataFrame,
        features: List[str],
        skip_incomplete_rows: bool,
    ):
        if not features:
            features = self.get_registered_features(feature_store)

        self.check_features_exist(feature_store, features)

        id_column = feature_store.columns[0]
        time_column = feature_store.columns[1]

        if len(targets.columns) != 2:
            raise Exception("Targets dataframe must have exactly two columns [id, date]")

        if id_column not in targets.columns:
            raise Exception(f"Id column {id_column} missing in targets dataframe")

        targets_time_column = list(set(targets.columns) - {id_column})[0]
        targets = targets.withColumnRenamed(targets_time_column, time_column)

        features_data = (
            feature_store.join(targets, on=[id_column, time_column])
            .join(rainbow_table, on=get_rainbow_table_hash_column().name)
            .withColumn("features_intersect", f.array_intersect(get_rainbow_table_features_column().name, f.array(*map(f.lit, features))))
            .withColumn("is_complete_row", f.size("features_intersect") == len(features))
        )

        has_incomplete_rows = len(features_data.filter(~f.col("is_complete_row")).limit(1).collect()) == 1

        if has_incomplete_rows and not skip_incomplete_rows:
            raise Exception("Features contain incomplete rows")

        return features_data.filter(f.col("is_complete_row")).select(id_column, time_column, *features)

    def check_features_exist(self, feature_store: DataFrame, features: List[str]):
        registered_features_list = self.get_registered_features(feature_store)
        unregistered_features = set(features) - set(registered_features_list)

        if unregistered_features != set():
            raise Exception(f"Features {','.join(unregistered_features)} not registered")

    def get_registered_features(self, feature_store: DataFrame):  # noqa
        return list(feature_store.columns[3:])
