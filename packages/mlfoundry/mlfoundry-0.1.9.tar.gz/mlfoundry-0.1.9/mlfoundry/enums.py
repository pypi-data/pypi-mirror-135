import enum


class FileFormat(enum.Enum):
    CSV = "csv"
    PARQUET = "parquet"


class ModelFramework(enum.Enum):
    SKLEARN = "sklearn"
    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"
    KERAS = "keras"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    FASTAI = "fastai"
    H2O = "h2o"
    ONNX = "onnx"
    SPACY = "spacy"
    STATSMODELS = "statsmodels"
    GLUON = "gluon"
    PADDLE = "paddle"


class DataSlice(enum.Enum):
    TRAIN = "train"
    VALIDATE = "validate"
    TEST = "test"
    PREDICTION = "prediction"


class ModelType(enum.Enum):
    BINARY_CLASSIFICATION = "binary_classification"
    MULTICLASS_CLASSIFICATION = "multiclass_classification"
    REGRESSION = "regression"
    TIMESERIES = "timeseries"
