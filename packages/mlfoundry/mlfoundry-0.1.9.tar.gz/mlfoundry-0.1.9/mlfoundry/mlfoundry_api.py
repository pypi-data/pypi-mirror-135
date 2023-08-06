"""
# TO independently test this module, you can run the example in the path
python examples/sklearn/iris_train.py

Besides running pytest
"""
import logging
from functools import partial
from typing import Optional

import mlflow
import pandas as pd
from mlflow.entities import ViewType
from mlflow.store.artifact.artifact_repository_registry import (
    _artifact_repository_registry,
)
from mlflow.tracking import MlflowClient
from mlflow.tracking._tracking_service.utils import _get_default_host_creds

from mlfoundry.artifact.truefoundry_artifact_repo import TruefoundryArtifactRepository
from mlfoundry.constants import *
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.mlfoundry_run import MlFoundryRun
from mlfoundry.tracking.truefoundry_rest_store import TruefoundryRestStore

log = logging.getLogger(__name__)


def overwrite_s3_artifact_repository(tracking_uri):
    get_cred = partial(_get_default_host_creds, tracking_uri)
    rest_store = TruefoundryRestStore(get_cred)
    artifact_repository = partial(TruefoundryArtifactRepository, rest_store=rest_store)
    _artifact_repository_registry.register("s3", artifact_repository)


def get_client(tracking_uri: Optional[str] = None, bucket_name: Optional[str] = None):
    if tracking_uri is None:
        tracking_uri = "file:" + os.path.abspath(MLRUNS_FOLDER_NAME)
    elif tracking_uri.startswith("file:"):
        tracking_uri = os.path.join(tracking_uri, MLF_FOLDER_NAME)
    else:
        overwrite_s3_artifact_repository(tracking_uri=tracking_uri)

    return MlFoundry(tracking_uri, bucket_name)


class MlFoundry:
    def __init__(self, db_uri: Optional[str] = None, bucket_name: Optional[str] = None):
        if bucket_name:
            self.__artifact_path = "s3://" + bucket_name
        else:
            self.__artifact_path = None
        self.__db_uri = db_uri

        try:
            mlflow.set_tracking_uri(db_uri)
        except MlflowException as e:
            err_msg = (
                f"Could not initialise mlfoundry object. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        self.mlflow_client = MlflowClient()

    def __get_or_create_experiment(self, experiment_name: str):
        """
        Creates a experiment and returns the experiment id. This experiment is to be passed into run.
        :param experiment_name: A unique experiment name
        :return: The experiment_id of created experiment

        Example:
        >> create_experiment('experiment 1')
        """

        try:
            if experiment_name in self.get_all_projects():
                experiment_id = mlflow.get_experiment_by_name(
                    experiment_name
                ).experiment_id
            else:
                experiment_id = mlflow.create_experiment(
                    experiment_name, artifact_location=self.__artifact_path
                )
        except MlflowException as e:
            err_msg = (
                f"Error happened in creating or getting experiment based on experiment name: "
                f"{experiment_name}. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        return experiment_id

    def __construct_run_name(self, project_name, run_name=None):
        if not run_name:
            # str(datetime.datetime.utcnow()) == '2022-01-11 23:39:13.179638'
            date_time_min = str(
                str(datetime.datetime.utcnow()).replace(" ", "_").split(".")[0]
            )
            run_name = f"{RUN_NAME_PREFIX}_{date_time_min}_utc"
        else:
            all_runs = self.get_all_runs(project_name)
            if run_name in all_runs[RUN_NAME_COL_NAME].values:
                date_time_min = str(
                    str(datetime.datetime.utcnow()).replace(" ", "_").split(".")[0]
                )
                run_name = f"{run_name}_{date_time_min}_utc"
        return run_name

    def get_all_projects(self):
        """
        Returns names of all the projects
        """
        try:
            experiments = self.mlflow_client.list_experiments(view_type=ViewType.ALL)
        except MlflowException as e:
            err_msg = (
                f"Error happened in fetching project names. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        projects = []
        for e in experiments:
            # Experiment ID 0 represents default project which we are removing.
            if e.experiment_id != "0":
                projects.append(e.name)

        return projects

    def rename_project(self, old_project_name: str, new_project_name: str):
        """
        Renames a project.
        :param old_project_name: Existing project name
        :param new_project_name: New Project name
        """

        try:
            experiment_id = self.mlflow_client.get_experiment_by_name(
                old_project_name
            ).experiment_id

            self.mlflow_client.rename_experiment(experiment_id, new_project_name)
        except MlflowException as e:
            err_msg = (
                f"Error happened in renaming project from {old_project_name} to "
                f"{new_project_name}. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

    def create_run(self, project_name: str, run_name: Optional[str] = None):
        """Creates a run for the given project_name(project_name).
        Each run will have a unique run_id.
        If run_name is not provided, then a name is generated automatically.
        Args:
            project_name (str): name of a project
            run_name (Optional[str]): name of the run
        Returns:
            MlFoundryRun: an MlFoundryRun with specified experiment and unique run_id

        Example:
        >> mlf_run = create_run('my_project')
        """

        if project_name == "" or (not isinstance(project_name, str)):
            raise MlFoundryException(
                f"project_name must be string type and not empty. "
                f"Got {type(project_name)} type with value {project_name}"
            )

        experiment_id = self.__get_or_create_experiment(project_name)
        run_name = self.__construct_run_name(project_name, run_name=run_name)

        run = self.mlflow_client.create_run(
            experiment_id, tags={RUN_NAME_COL_NAME: run_name}
        )
        mlf_run_id = run.info.run_id

        mlf_run = MlFoundryRun(experiment_id, mlf_run_id)
        log.info(f"Run is created with id {mlf_run_id} and name {run_name}")
        return mlf_run

    def get_run(self, run_id: str):
        """Given the run_id returns the Python MlFoundryRun object that is created already.

        Args:
            run_id (str): run_id that was created already.

        Returns:
            MlFoundryRun: returns the run object that was created already.

        Example:
        >> run = get_run(<run_id>)
        """
        if run_id == "" or (not isinstance(run_id, str)):
            raise MlFoundryException(
                f"run_id must be string type and not empty. "
                f"Got {type(run_id)} type with value {run_id}"
            )

        run = self.mlflow_client.get_run(run_id)
        experiment_id = run.info.experiment_id
        return MlFoundryRun(experiment_id, run.info.run_id)

    def get_all_runs(self, project_name: str):
        """Returns all the run that was created by the user under the project project_name

        Returns:
            pd.DataFrame: dataframe with two columns- run_id and run_name
        """
        if project_name == "" or (not isinstance(project_name, str)):
            raise MlFoundryException(
                f"project_name must be string type and not empty. "
                f"Got {type(project_name)} type with value {project_name}"
            )

        experiment = self.__get_or_create_experiment(project_name)

        try:
            all_runs = self.mlflow_client.list_run_infos(
                experiment, run_view_type=ViewType.ALL
            )
        except MlflowException as e:
            err_msg = f"Error happened in while fetching runs for project {project_name}. Error details: {e.message}"
            raise MlFoundryException(err_msg) from e

        runs = []

        for run in all_runs:
            try:
                with mlflow.start_run(
                    run_id=run.run_id, experiment_id=experiment
                ) as run1:
                    run1_tags = run1.data.tags
                    if RUN_NAME_COL_NAME in run1_tags.keys():
                        run_name = run1_tags[RUN_NAME_COL_NAME]
                    else:
                        run_name = ""

                runs.append((run.run_id, run_name))
            except MlflowException as e:
                log.warning(
                    f"Could not fetch details of run with run_id {run.run_id}. "
                    f"Skipping this one. Error details: {e.message}. "
                )
                continue

        return pd.DataFrame(runs, columns=[RUN_ID_COL_NAME, RUN_NAME_COL_NAME])

    @staticmethod
    def get_tracking_uri():
        return mlflow.tracking.get_tracking_uri()
