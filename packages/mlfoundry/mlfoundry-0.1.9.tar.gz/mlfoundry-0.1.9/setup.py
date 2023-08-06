# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlfoundry',
 'mlfoundry.artifact',
 'mlfoundry.cli',
 'mlfoundry.frameworks',
 'mlfoundry.metrics',
 'mlfoundry.tracking',
 'mlfoundry.tracking.entities']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.1',
 'fastparquet>=0.7.2,<0.8.0',
 'matplotlib>=3.0.3',
 'mlflow>=1.14',
 'numpy>=1.17.0',
 'pandas>=1.0.0',
 'pipreqs>=0.4.11,<0.5.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'pyarrow>=5.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.5.4,<2.0.0',
 'shap>=0.40.0,<0.41.0',
 'whylogs>=0.6.15']

entry_points = \
{'console_scripts': ['mlfoundry = '
                     'mlfoundry.cli.cli_interface:create_mlfoundry_cli']}

setup_kwargs = {
    'name': 'mlfoundry',
    'version': '0.1.9',
    'description': 'Building logger package',
    'long_description': "# MlFoundry\n\n![](https://github.com/MyName/my-project/workflows/Project%20Tests/badge.svg)\n\nThis guide is to give an idea of how you can log metrics, paramaters, predictions, models, dataset using MlFoundry. MlFoundry supports logging above mentioned logs to S3 asynchronously.\n\n## API Workflow:\n\nUsing mlfoundry you ca create multiple projects and each projects can have multiple run.\n\n**Example**\n\n1. Project 1\n   - run 1\n   - run 2\n2. Project 2\n   - run 1\n   - run 2\n   - run 3\n   - run 4\n\nEach run under each project will have a unique run_id.\n\n## Quickstart\n\n### 1. Install mlfoundry\n\n```\n# Install via pip\npip install mlfoundry --extra-index-url https://api.packagr.app/public\n```\n\n### 2. Setup AWS credentials\n\nTo setup AWS credentials MlLogs_foundry's CLI can be used. AWS credentials are required to store the artifacts like model, dataset, whylogs_metrics etc in S3 Bucket.\n\nThe CLI requires AWS credentials(SECRET_ACCESS_KEY, ACCESS_KEY_ID)\n\nAll the credentials can be set by running:\n\n`mlfoundry init`\n\n### 3. Initialise mlfoundry\n\nCreate an project and use the project_name to create a run:\n\n```python\n import mlfoundry as mlf\n\n # create a run\n mlf_run = mlf.create_run(project_name=<project-name>)\n```\n\nIf you want to use a previously created run:\n\n```python\n# printing all the runs available and get the run_id\nshow_all_runs()\n\nrun = get_run(run_id=<run_id>)\n```\n\n### 4. Start logging\n\n**To log a model:**\n\n```python\nrun.log_model(sklearn_model, framework=mlf.ModelFramework.SKLEARN)\n```\n\n**To log parameters:**\n\n```python\nrun.log_params({'learning_rate':0.01,\n                  'n_epochs:10'\n                  })\n```\n\n**To log metrics:**\n\n```python\nrun.log_metrics({'accuracy':87,\n                  'f1_score':0.84,\n                  })\n```\n\n**Log predictions synchronously:**\n\nfeature_df: a pd.DataFrame, the input given to the model to make predictions\n\npredictions: must be a list or pd.Series\n\nTo log predictions synchronously:\n\n```python\nrun.log_predictions(self, feature_df, predictions)\n```\n\nTo log predictions asynchronously:\n\n```python\nresponses = run.log_predictions_async(self, feature_df, predictions)\n\n#### To confirm that the log request completed successfully, await for futures to resolve: This is a blocking call\nimport concurrent.futures as cf\nfor response in cf.as_completed(responses):\n  res = response.result()\n```\n\nUsers can additionaly pass in feature_names argument which is a list of feture names for feature_df.\n\n# To release as Python package\n\nUse Github Releases to create a tag on main and release it. This will trigger the workflow and publish the pip package\n\nTags must be of format `vx.x.x`, example `v0.1.0`\n\n# Development instructions\n\n```\ngit clone https://github.com/truefoundry/mlfoundry.git\ncd mlfoundry\nvirtualenv venv\nsource venv/bin/activate\npip install poetry\npoetry install\npre-commit install\n```\n",
    'author': 'Abhishek Choudhary',
    'author_email': 'abhichoudhary06@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/truefoundry/mlfoundry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
