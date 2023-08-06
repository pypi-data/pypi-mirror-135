import json
import logging
import pickle
import time

import dateutil.parser
import mlflow
import numpy as np
import pandas as pd
import whylogs
from mlflow.entities import Metric, Param, RunTag
from mlflow.tracking import MlflowClient

from mlfoundry.async_executer import AsyncExecuter
from mlfoundry.constants import *
from mlfoundry.enums import *
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.frameworks import *
from mlfoundry.metrics import (
    BinaryClassificationMetrics,
    MultiClassClassificationMetrics,
    RegressionMetrics,
    TimeSeriesMetrics,
)
from mlfoundry.run_utils import download_artifact
from mlfoundry.schema import Schema

log = logging.getLogger(__name__)

MODEL_TYPE_TO_CLASS_MAP = {
    ModelType.BINARY_CLASSIFICATION: BinaryClassificationMetrics,
    ModelType.MULTICLASS_CLASSIFICATION: MultiClassClassificationMetrics,
    ModelType.REGRESSION: RegressionMetrics,
    ModelType.TIMESERIES: TimeSeriesMetrics,
}


class MlFoundryRun:

    S3_MODELS_PATH = "models"
    S3_PREDICTIONS_PATH = "predictions"
    S3_DATASET_PATH = "datasets"
    S3_STATS_PATH = "stats"
    S3_WHYLOGS_PATH = "whylogs"
    S3_METRICS_PATH = "multi_dimensional_metrics"

    def __init__(self, experiment_id, run_id):
        self.experiment_id = str(experiment_id)
        self.experiment = mlflow.get_experiment(self.experiment_id)
        self.run_id = run_id
        # TODO (nikunjbjj): Refactor this code as per
        self.model_framework_class = {
            ModelFramework.SKLEARN: SkLearnRegistry,
            ModelFramework.TENSORFLOW: TensorflowRegistry,
            ModelFramework.PYTORCH: PyTorchRegistry,
            ModelFramework.KERAS: KerasRegistry,
            ModelFramework.XGBOOST: XGBoostRegistry,
            ModelFramework.LIGHTGBM: LightGBMRegistry,
            ModelFramework.FASTAI: FastAIRegistry,
            ModelFramework.H2O: H2ORegistry,
            ModelFramework.ONNX: ONNXRegistry,
            ModelFramework.SPACY: SpacyRegistry,
            ModelFramework.STATSMODELS: StatsModelsRegistry,
            ModelFramework.GLUON: GluonRegistry,
            ModelFramework.PADDLE: PaddleRegistry,
        }
        self.exec = AsyncExecuter()
        self.mlflow_client = MlflowClient()
        self.model_uri = "runs:/" + str(self.run_id) + "/" + self.S3_MODELS_PATH

    def __runname_in_predictions(self, run_id):
        """
        Helper function to check if user has already logged predictions and if it is stored in the local system.
        If the predcitions has been logged already for the run_id, the file name is returneed
        """
        temp_pred_file = os.listdir(RUN_PREDICTIONS_FOLDER)
        file_exists = False
        prev_df_filename = None
        prev_df_fileformat = None
        for file in temp_pred_file:
            if run_id in file:
                file_exists = True
                prev_df_filename = os.path.join(RUN_PREDICTIONS_FOLDER, file)
                _, prev_df_fileformat = os.path.splitext(
                    prev_df_filename
                )  # returns extension, eg: .parquet
                # removing . from extension
                prev_df_fileformat = prev_df_fileformat[1:]
                break
        return file_exists, prev_df_filename, prev_df_fileformat

    def __get_dataset_path(self, data_slice: DataSlice, fileformat: FileFormat = None):
        if fileformat:
            return (
                str(self.run_id) + "_" + data_slice.value + "." + str(fileformat.value)
            )  # with extension
        else:
            return str(self.run_id) + "_" + data_slice.value  # without extension

    def log_model(self, model, framework: ModelFramework):
        """logs a model to s3 given a model object along with the framework
        Args:
            model : model object in a particular framework
            framework (str): one of the framework
        Example:
        >> log_model(sklearn_model, ModelFramework.SKLEARN)
        """

        try:
            artifacts = self.mlflow_client.list_artifacts(self.run_id)
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        for artifact in artifacts:
            if MlFoundryRun.S3_MODELS_PATH in artifact.path:
                raise MlFoundryException(f"Model already logged, cannot overwrite")

        mlflow.end_run()
        with mlflow.start_run(
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            tags={"modelFramework": framework.value},
        ) as run:
            model_framework_class_instance = self.model_framework_class[framework]()
            model_framework_class_instance.log_model(
                model, artifact_path=MlFoundryRun.S3_MODELS_PATH
            )

        log.info("Model logged Successfully")

    def log_dataset(
        self, df, data_slice: DataSlice, fileformat: FileFormat = FileFormat.PARQUET
    ):
        """Logs a dataset to s3,
        We can only log one dataset for a slice per run.
        If attempt to log dataset more than once an error is thrown out.
        Args:
            df: Dataset to upload
            data_slice: data slice   type of ‘df’ argument
            fileformat: (Default - FileFormat.PARQUET) - format of the file for the dataset to be saved
        Example:
        >> log_dataset(dataset_df, DataSlice.TRAIN, FileFormat.PARQUET)
        """

        if not isinstance(df, pd.DataFrame):
            raise MlFoundryException("Only pandas dataframe is supported")

        artifact_name = self.__get_dataset_path(data_slice, fileformat)

        artifacts = self.mlflow_client.list_artifacts(self.run_id)
        for artifact in artifacts:
            if self.__get_dataset_path(data_slice) in artifact.path:
                raise MlFoundryException(
                    f"Dataset {str(self.run_id)}_{data_slice.value} already logged, cannot overwrite"
                )

        RUN_DATASET_FOLDER.mkdir(parents=True, exist_ok=True)
        filename = os.path.join(RUN_DATASET_FOLDER, artifact_name)

        if fileformat == FileFormat.PARQUET:
            df.to_parquet(filename)

        elif fileformat == FileFormat.CSV:
            df.to_csv(filename)

        try:
            self.mlflow_client.log_artifact(self.run_id, filename)
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        os.remove(filename)

    def log_metrics(self, metric_dict: dict):
        """Logs the metrics given metric_dict that has metric name as key and metric value as value
        Args:
            metric_dict (dict): metric_dict that has metric name as key and metric value as value
        Examples:
        >> log_metric({'accuracy':0.91, 'f1_score:0.5'})
        """

        try:
            # mlfowclient doesnt have log_metrics api, so we have to use log_batch, This is what internally used by mlflow.log_metrics
            timestamp = int(time.time() * 1000)
            metrics_arr = [
                Metric(key, value, timestamp, 0) for key, value in metric_dict.items()
            ]
            self.mlflow_client.log_batch(
                run_id=self.run_id, metrics=metrics_arr, params=[], tags=[]
            )
            # self.mlflow_client.log_metrics
            # with self.mlflow_run:
            #     mlflow.log_metrics(metric_dict)
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        log.info("Metrics logged successfully")

    def log_params(self, param_dict: dict):
        """Logs the parameter given param_dict that has param name as key and param value as value
        Args:
            param_dict (dict): param_dict that has param name as key and param value as value
        Examples:
        >> log_params({'learning_rate':0.01, 'n_epochs:10'})
        """

        try:
            # mlfowclient doesnt have log_params api, so we have to use log_batch, This is what internally used by mlflow.log_params
            params_arr = [Param(key, str(value)) for key, value in param_dict.items()]
            self.mlflow_client.log_batch(
                run_id=self.run_id, metrics=[], params=params_arr, tags=[]
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        log.info("Parameters logged successfully")

    def log_predictions_async(
        self, feature_df, predictions, fileformat=FileFormat.CSV, feature_names=None
    ):
        """Logs prediction to s3 synchronously
        Args:
            feature_df (pd.DataFrame): input that is given to the model in the form of csv
            predictions (list or pd.Series): predictions for the given input
            fileformat (str, optional): fileformat to store the prediction. Defaults to 'csv'.
            feature_names (list, optional): list of feature names. Defaults to None.
        Returns:
            futures: Lits of future object that can we awaited
        """

        futures = []
        futures.append(
            self.exec.submit(
                self.log_predictions, feature_df, predictions, fileformat, feature_names
            )
        )
        return futures

    def log_predictions(
        self,
        feature_df,
        predictions,
        fileformat: FileFormat = FileFormat.CSV,
        feature_names=None,
    ):
        """Logs prediction to s3 synchronously
        Args:
            feature_df (pd.DataFrame): input that is given to the model in the form of csv
            predictions (list or pd.Series): predictions for the given input
            fileformat (str, optional): fileformat to store the prediction. Defaults to 'csv'.
            feature_names (list, optional): list of feature names. Defaults to None.
        """
        # Do all necessary validations
        self.__log_prediction_validation(feature_df, predictions, feature_names)

        if isinstance(predictions, pd.Series):
            predictions = predictions.tolist()

        final_df = feature_df.copy()
        final_df["predictions"] = predictions

        current_time = datetime.datetime.now().strftime(TIME_FORMAT)
        format_value = fileformat.value
        pred_file_path = os.path.join(
            RUN_PREDICTIONS_FOLDER,
            str(self.run_id) + "_" + current_time + "." + format_value,
        )

        RUN_TMP_FOLDER.mkdir(exist_ok=True, parents=True)
        RUN_PREDICTIONS_FOLDER.mkdir(exist_ok=True, parents=True)

        # check if there is a prediction file corresponding to the run_id
        (
            file_exists,
            prev_df_filename,
            prev_df_fileformat,
        ) = self.__runname_in_predictions(str(self.run_id))

        # if run_id exists in temp/pred folder
        if file_exists:
            if format_value != prev_df_fileformat:
                raise MlFoundryException(
                    f"Given fileformat({format_value}) and stored fileformat({prev_df_fileformat}) doesn't match"
                )
            elif format_value == FileFormat.CSV.value:
                prev_df = pd.read_csv(prev_df_filename)
            elif format_value == FileFormat.PARQUET.value:
                prev_df = pd.read_parquet(prev_df_filename)
                final_df.columns = final_df.columns.astype(str)

            # pred_df_filename will be like: 'model1_2021-10-27 00:18:03.csv', from here we are extracting time
            prev_df_time = os.path.splitext(prev_df_filename.split("_")[-1])
            prev_df_time = prev_df_time[0]
            prev_df_time = dateutil.parser.parse(prev_df_time)

            current_df_time = datetime.datetime.now()
            final_df = prev_df.append(final_df)
            pred_file_path = prev_df_filename

        if format_value == FileFormat.CSV.value:
            final_df.to_csv(pred_file_path, index=False)
        else:
            final_df.columns = final_df.columns.astype(str)
            final_df.to_parquet(pred_file_path, index=False)
        # check if the time limit exceeds or size limit exceeds, if it exceeds directly send it to S3
        if (file_exists and current_df_time - prev_df_time > TIME_LIMIT_THRESHOLD) or (
            os.path.getsize(pred_file_path) > FILE_SIZE_LIMIT_THRESHOLD
        ):
            self.__save_predictions_s3(
                pred_file_path,
                str(self.run_id)
                + "_"
                + datetime.datetime.now().strftime(TIME_FORMAT)
                + "."
                + format_value,
            )
            os.remove(pred_file_path)
            log.info("Predictions logged successfully")

    def __compute_whylogs_stats(self, df):

        if not isinstance(df, pd.DataFrame):
            raise MlFoundryException(
                f"df is expexted to be pd.DataFrame but got {str(type(df))}"
            )

        profile_file_name = (
            "profile" + "_" + datetime.datetime.now().strftime(TIME_FORMAT) + ".bin"
        )
        session = whylogs.get_or_create_session()
        profile = session.new_profile()
        profile.track_dataframe(df)
        profile.write_protobuf(profile_file_name)

        try:
            self.mlflow_client.set_tag(self.run_id, "whylogs", True)
            self.mlflow_client.log_artifact(
                self.run_id,
                profile_file_name,
                artifact_path=MlFoundryRun.S3_WHYLOGS_PATH,
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        if os.path.exists(profile_file_name):
            os.remove(profile_file_name)

    def __log_prediction_validation(self, feature_df, predictions, feature_names):
        """validation for log_prediction method
        Args:
            feature_df (pd.DataFrame): input that is given to the model in the form of csv
            predictions (list or pd.Series): predictions for the given input
            feature_names (list, optional): list of feature names. Defaults to None.
        Returns:
            bool: False if the validation fails
        """
        # check if feature df is a df
        if not isinstance(feature_df, pd.DataFrame):
            raise MlFoundryException(
                f"Expected pd.DataFrame but got {str(type(feature_df))}"
            )

        if not isinstance(predictions, list) or isinstance(predictions, pd.Series):
            raise MlFoundryException(
                f"Expected pd.Series or list but got {str(type(predictions))}"
            )
        # check if len of predictions and feature_df matches
        if len(feature_df) != len(predictions):
            raise MlFoundryException(
                f"size of feature_df({feature_df.shape[0], feature_df.shape[1]}) doesn't match with size of predictions({len(predictions)})"
            )

        # if feature_name is None, get column_names from feature_df
        if feature_names is None:
            column_names = list(feature_df.columns)
        else:
            # check if number of columns of feature df and feature name is same
            if len(feature_names) != feature_df.shape[1]:
                raise MlFoundryException(
                    f"size of feature_df({feature_df.shape[0], feature_df.shape[1]}) doesn't match with size of feature_names({len(feature_names)})"
                )
            column_names = feature_names

        # TODO(Rizwan): usig column_names check here if this column names matches with prediction data that is logged in already

    def __save_predictions_s3(self, file, filename_s3):

        try:
            self.mlflow_client.log_artifact(
                self.run_id, file, artifact_path=MlFoundryRun.S3_PREDICTIONS_PATH
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

    def log_dataset_stats(
        self,
        df,
        data_slice: DataSlice,
        data_schema: Schema,
        model_type: ModelType,
        shap_values=None,
    ):
        if not isinstance(df, pd.DataFrame):
            raise MlFoundryException(f"Expected pd.DataFrame but got {str(type(df))}")

        if not data_schema.actual_column_name:
            raise MlFoundryException(f"Schema.actual_column_name cannot be None")
        elif not data_schema.prediction_column_name:
            raise MlFoundryException(f"Schema.prediction_column_name cannot be None")
        elif data_schema.feature_column_names is None:
            raise MlFoundryException(f"Schema.feature_column_names cannot be None")
        elif not isinstance(data_schema.feature_column_names, list):
            raise MlFoundryException(
                f"data_schema.feature_column_names should be of type list, cannot be {type(data_schema.feature_column_names)}"
            )

        self.__compute_whylogs_stats(df[set(data_schema.feature_column_names)])

        if model_type in [
            ModelType.BINARY_CLASSIFICATION,
            ModelType.MULTICLASS_CLASSIFICATION,
        ]:
            class_names = None
            prediction_col_dtype, actual_col_dtype = (
                df[data_schema.prediction_column_name].dtype,
                df[data_schema.actual_column_name].dtype,
            )
            if prediction_col_dtype == object and actual_col_dtype != object:
                raise MlflowException(
                    "Both predictions column and actual column has to be of same datatype, either string or number"
                )
            elif prediction_col_dtype != object and actual_col_dtype == object:
                raise MlflowException(
                    "Both predictions column and actual column has to be of same datatype, either string or number"
                )
            elif prediction_col_dtype == object and actual_col_dtype == object:
                actual_class_names = df[data_schema.actual_column_name].unique()
                prediction_class_name = df[data_schema.prediction_column_name].unique()
                class_names = list(set(actual_class_names) | set(prediction_class_name))
                df[data_schema.actual_column_name] = df[
                    data_schema.actual_column_name
                ].apply(lambda x: class_names.index(x))
                df[data_schema.prediction_column_name] = df[
                    data_schema.prediction_column_name
                ].apply(lambda x: class_names.index(x))

        unique_count_dict = {}
        if model_type in [
            ModelType.BINARY_CLASSIFICATION,
            ModelType.MULTICLASS_CLASSIFICATION,
        ]:
            unique_count_dict[data_schema.prediction_column_name] = np.unique(
                df[data_schema.prediction_column_name].to_list(), return_counts=True
            )
            unique_count_dict[data_schema.actual_column_name] = np.unique(
                df[data_schema.actual_column_name].to_list(), return_counts=True
            )
        elif model_type == ModelType.REGRESSION:
            session = whylogs.get_or_create_session()
            profile = session.new_profile()
            profile.track_dataframe(
                df[[data_schema.actual_column_name, data_schema.prediction_column_name]]
            )
            unique_count_dict[ACTUAL_PREDICTION_COUNTS] = profile.flat_summary()["hist"]

        if data_schema.categorical_feature_column_names:
            for feature in data_schema.categorical_feature_column_names:
                unique_count_dict[feature] = np.unique(
                    df[feature].to_list(), return_counts=True
                )

        unique_count_name = "unique_count" + "_" + str(data_slice.value) + ".pkl"
        RUN_STATS_FOLDER.mkdir(parents=True, exist_ok=True)
        unique_count_path = os.path.join(RUN_STATS_FOLDER, unique_count_name)

        with open(unique_count_path, "wb") as fp:
            pickle.dump(unique_count_dict, fp)

        schema_json_name = "schema" + "_" + str(data_slice.value) + ".json"
        schema_json_path = os.path.join(RUN_STATS_FOLDER, schema_json_name)

        with open(schema_json_path, "w") as outfile:
            json.dump(data_schema.__dict__, outfile)

        if (
            model_type
            in [ModelType.BINARY_CLASSIFICATION, ModelType.MULTICLASS_CLASSIFICATION]
            and class_names is not None
        ):
            class_names_path = f"class_names_{data_slice.value}.pkl"
            class_names_path = RUN_STATS_FOLDER / class_names_path
            with open(class_names_path, "wb") as fp:
                pickle.dump(class_names, fp)

        metrics_class = MODEL_TYPE_TO_CLASS_MAP[model_type]()
        metrics_dict = {}

        if data_schema.prediction_probability_column_name:
            metrics_dict = metrics_class.compute_metrics(
                df[set(data_schema.feature_column_names)],
                df[data_schema.prediction_column_name].to_list(),
                df[data_schema.actual_column_name].to_list(),
                df[data_schema.prediction_probability_column_name].to_list(),
            )
        else:
            metrics_dict = metrics_class.compute_metrics(
                df[set(data_schema.feature_column_names)],
                df[data_schema.prediction_column_name].to_list(),
                df[data_schema.actual_column_name].to_list(),
            )
        # non-multi dimensional metrics
        metrics_dict_with_data_slice = {}

        for key in metrics_dict[NON_MULTI_DIMENSIONAL_METRICS].keys():
            new_key = "pre_computed_" + key + "_" + str(data_slice.value)
            metrics_dict_with_data_slice[new_key] = metrics_dict[
                NON_MULTI_DIMENSIONAL_METRICS
            ][key]

        if shap_values is not None:
            tag_key = "data_stats_and_shap_" + data_slice.value
        else:
            tag_key = "data_stats_" + data_slice.value

        self.mlflow_client.set_tag(self.run_id, "modelType", model_type.value)
        self.mlflow_client.set_tag(self.run_id, tag_key, True)
        self.log_metrics(metrics_dict_with_data_slice)

        RUN_METRICS_FOLDER.mkdir(parents=True, exist_ok=True)
        multi_dimension_metric_file = (
            "pre_computed_"
            + MULTI_DIMENSIONAL_METRICS
            + "_"
            + str(data_slice.value)
            + ".pkl"
        )
        multi_dimension_metric_file_path = os.path.join(
            RUN_METRICS_FOLDER, multi_dimension_metric_file
        )

        with open(multi_dimension_metric_file_path, "wb") as fp:
            pickle.dump(metrics_dict[MULTI_DIMENSIONAL_METRICS], fp)

        if model_type == ModelType.TIMESERIES:
            actuals_predictions_filename = (
                "actuals_predictions_" + str(data_slice.value) + ".parquet"
            )
            actuals_predictions_filepath = os.path.join(
                RUN_STATS_FOLDER, actuals_predictions_filename
            )
            df[
                [data_schema.prediction_column_name, data_schema.actual_column_name]
            ].to_parquet(actuals_predictions_filepath)

        try:

            # with self.mlflow_run as run:
            self.mlflow_client.log_artifact(
                self.run_id, unique_count_path, artifact_path=MlFoundryRun.S3_STATS_PATH
            )
            self.mlflow_client.log_artifact(
                self.run_id,
                multi_dimension_metric_file_path,
                artifact_path=MlFoundryRun.S3_METRICS_PATH,
            )
            self.mlflow_client.log_artifact(
                self.run_id, schema_json_path, artifact_path=MlFoundryRun.S3_STATS_PATH
            )
            if (
                model_type
                in [
                    ModelType.BINARY_CLASSIFICATION,
                    ModelType.MULTICLASS_CLASSIFICATION,
                ]
                and class_names is not None
            ):
                self.mlflow_client.log_artifact(
                    self.run_id,
                    class_names_path,
                    artifact_path=MlFoundryRun.S3_STATS_PATH,
                )
            if model_type == ModelType.TIMESERIES:
                self.mlflow_client.log_artifact(
                    self.run_id,
                    actuals_predictions_filepath,
                    artifact_path=MlFoundryRun.S3_STATS_PATH,
                )
                os.remove(actuals_predictions_filepath)
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        os.remove(multi_dimension_metric_file_path)
        os.remove(schema_json_path)
        os.remove(unique_count_path)

        if shap_values is not None:
            self.__log_shap_values(
                df[set(data_schema.feature_column_names)], shap_values, data_slice
            )

        log.info("Dataset stats have been successfully computed and logged")

    def __log_shap_values(self, df, shap_values: list, data_slice: DataSlice):

        if not isinstance(df, pd.DataFrame):
            raise MlFoundryException(f"Expected pd.DataFrame but got {str(type(df))}")

        artifact_name = str(self.run_id) + "_" + str(data_slice.value) + "_shap.pkl"
        RUN_STATS_FOLDER.mkdir(parents=True, exist_ok=True)
        filename = os.path.join(RUN_STATS_FOLDER, artifact_name)

        with open(filename, "wb") as fp:
            pickle.dump(shap_values, fp)

        try:
            self.mlflow_client.log_artifact(
                self.run_id, filename, artifact_path=MlFoundryRun.S3_STATS_PATH
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        os.remove(filename)

    def __get_artifact(self, run_id, artifact_name, dest_path):
        try:
            return self.mlflow_client.download_artifacts(
                run_id, artifact_name, dest_path
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

    def get_dataset(self, data_slice: DataSlice):

        artifacts = self.mlflow_client.list_artifacts(self.run_id)

        dataset_file_name = None
        GET_RUN_DATASET_FOLDER.mkdir(parents=True, exist_ok=True)

        for artifact in artifacts:
            if self.__get_dataset_path(data_slice) in artifact.path:
                self.__get_artifact(self.run_id, artifact.path, GET_RUN_DATASET_FOLDER)
                dataset_file_name = artifact.path
                break

        if dataset_file_name:
            ext = dataset_file_name.split(".")[-1]
            dataset_file_path = os.path.join(GET_RUN_DATASET_FOLDER, dataset_file_name)

            dataset_df = None
            if ext == FileFormat.PARQUET.value:
                dataset_df = pd.read_parquet(dataset_file_path)
            elif ext == FileFormat.CSV.value:
                dataset_df = pd.read_csv(dataset_file_path)

            log.info(f"Dataset saved to {dataset_file_path}")
            return dataset_df
        else:
            raise MlFoundryException("Dataset not logged!")

    def get_metrics(self):
        ## Ending any run that is active to prevent mlflow from throwing error
        run = self.mlflow_client.get_run(self.run_id)
        return run.data.metrics

    def get_params(self):
        ## Ending any run that is active to prevent mlflow from throwing error
        run = self.mlflow_client.get_run(self.run_id)
        return run.data.params

    def download_logged_predictions(self):
        artifacts = self.mlflow_client.list_artifacts(self.run_id)

        dataset_file_name = None
        GET_RUN_PREDICTIONS_FOLDER.mkdir(parents=True, exist_ok=True)

        for artifact in artifacts:
            if self.S3_PREDICTIONS_PATH in artifact.path:
                self.__get_artifact(self.run_id, artifact.path, GET_RUN_TMP_FOLDER)
                dataset_file_name = artifact.path
                break

        if dataset_file_name:
            return os.path.abspath(GET_RUN_PREDICTIONS_FOLDER)
        else:
            raise MlFoundryException("Predictions not logged!")

    def get_model(self, dest_path: str = None, **kwargs):
        artifacts = self.mlflow_client.list_artifacts(self.run_id)
        model_exists = False
        model_file_path = None
        for artifact in artifacts:
            if MlFoundryRun.S3_MODELS_PATH in artifact.path:
                model_exists = True
                model_file_path = artifact.path
                break

        if not model_exists:
            raise MlFoundryException("Model is not logged")

        run = self.mlflow_client.get_run(self.run_id)
        run_tags = run.data.tags

        framework = ModelFramework(run_tags.get("modelFramework"))

        if framework is None:

            raise MlFoundryException("Invalid Framework found")

        if framework == ModelFramework.TENSORFLOW:
            self.model_uri = model_file_path

        model_framework_class_instance = self.model_framework_class[framework]()
        return model_framework_class_instance.load_model(
            self.model_uri,
            dest_path=dest_path,
            mlflow_client=self.mlflow_client,
            run_id=self.run_id,
            **kwargs,
        )
