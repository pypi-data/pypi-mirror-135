from mlflow.exceptions import MlflowException


class MlFoundryException(MlflowException):
    def __init__(self, message):
        self.message = message
