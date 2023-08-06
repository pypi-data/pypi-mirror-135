import mlflow

from mlfoundry.exceptions import MlflowException, MlFoundryException


def download_artifact(mlflow_client, run_id, artifact_name, dest_path):
    try:
        return mlflow_client.download_artifacts(run_id, artifact_name, dest_path)
    except MlflowException as e:
        raise MlFoundryException(e.message).with_traceback(e.__traceback__) from None
