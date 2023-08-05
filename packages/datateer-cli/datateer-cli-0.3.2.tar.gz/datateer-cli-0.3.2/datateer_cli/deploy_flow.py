import glob
import logging
import os
import tempfile
from importlib import find_loader, import_module
from pathlib import Path
from shutil import copy, copytree, ignore_patterns
from typing import Dict

import boto3
import click
import pathspec
import yaml

from datateer_cli.pipeline import settings

DOCKERFILE_TEMPLATES_DIR = Path(__file__).parent.joinpath("flow")


def do_deploy(flow, environment="staging", debug=False):
    # expensive loads, so defer until now
    from prefect.client.client import Client
    from prefect.executors import LocalExecutor

    # from prefect.environments import LocalEnvironment
    from prefect.run_configs import ECSRun
    from prefect.storage import Docker

    dockerfile_path = copy(os.path.join(DOCKERFILE_TEMPLATES_DIR, "Dockerfile"), ".")
    copy(os.path.join(DOCKERFILE_TEMPLATES_DIR, ".dockerignore"), ".")

    if os.getenv("MELTANO_DATABASE_URI") is None:
        print("MELTANO_DATABASE_URI is None")
    else:
        print(
            f'MELTANO_DATABASE_URI is populated with value {os.getenv("MELTANO_DATABASE_URI")[0:8]}***'
        )

    flow.storage = Docker(
        registry_url=image_registry_url(),
        python_dependencies=["boto3"],
        dockerfile=dockerfile_path,
        image_tag="latest",
        env_vars={
            "DATATEER_ENV": environment,
            # "AWS_DEFAULT_REGION": os.environ["AWS_DEFAULT_REGION"],
            # "S3_PREFECT_RESULTS_BUCKET": os.environ["S3_PREFECT_RESULTS_BUCKET"],
        },
        build_kwargs={
            "buildargs": {
                # during the build process, the build script runs "meltano install." By default, this command runs against an internal Sqlite database
                # To make sure this runs against the production meltano database, we ensure this env var exists and contains the connection string
                "MELTANO_DATABASE_URI": os.getenv("MELTANO_DATABASE_URI"),
                "DATATEER_DEPLOY_KEY_PREFECT_LIB": os.environ[
                    "DATATEER_DEPLOY_KEY_PREFECT_LIB"
                ],
            }
        },
    )

    task_definition = {
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE"],
        "executionRoleArn": f"arn:aws:iam::{os.environ['AWS_ACCOUNT_ID']}:role/ecsTaskExecutionRole",
        "taskRoleArn": f"arn:aws:iam::{os.environ['AWS_ACCOUNT_ID']}:role/ecsTaskRole",
        "containerDefinitions": [
            {
                "name": "flow",
                # "logConfiguration": { # this won't create the log group, so we can't reference it until we have some mechanism to create it
                #     "logDriver": "awslogs",
                #     "options": {
                #         "awslogs-group": f"/datateer/pipelines/{flow.name}",
                #         "awslogs-region": os.environ["AWS_DEFAULT_REGION"],
                #         "awslogs-stream-prefix": "prefect-agent",
                #     },
                # },
            }
        ],
    }
    flow.run_config = ECSRun(
        cpu="1 vcpu",  # 1 vcpu == 1 GB. https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html
        memory="8 GB",
        task_definition=task_definition,
        env={
            "DATATEER_ENV": environment,
            "AWS_DEFAULT_REGION": os.environ["AWS_DEFAULT_REGION"],
            "S3_PREFECT_RESULTS_BUCKET": os.environ["S3_PREFECT_RESULTS_BUCKET"],
        },
        run_task_kwargs={
            "networkConfiguration": {
                "awsvpcConfiguration": {
                    "subnets": [
                        settings.get_parameter("/pipeline/subnet_1"),
                        settings.get_parameter("/pipeline/subnet_2"),
                    ],
                    "securityGroups": [
                        settings.get_parameter("/pipeline/security_group")
                    ],
                    "assignPublicIp": "DISABLED",
                }
            }
        },
    )

    flow.executor = LocalExecutor()

    try:
        register(flow, environment)
    except ValueError:
        Client().create_project(os.environ["CLIENT_CODE"])
        register(flow, environment)


def register(flow, environment):
    import datateer_cli.docker_util as d

    d.docker_login()
    d.ensure_repository_exists(flow.name)
    flow.register(
        project_name=os.environ["CLIENT_CODE"],
        # add the environment label and the client label to restrict which agents will run this
        labels=[environment, os.environ["CLIENT_CODE"]],
    )


def image_registry_url(include_https=False):
    """Builds a well formed docker registry URL

    Arguments:
        account_id {string} -- the AWS account ID
        region {string} -- the AWS region e.g. us-east-1 or eu-west-1

    Keyword Arguments:
        include_https {bool} -- True to include the https:// prefix, false to leave off (default: {False})

    Returns:
        string -- A well formed docker registry URL
    """
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    registry = f'{account_id}.dkr.ecr.{os.getenv("AWS_DEFAULT_REGION")}.amazonaws.com'
    return f"https://{registry}" if include_https else registry


# def validate_environment(ctx, name, environment):
#     path = '.env' if environment == 'local' else f'.env.{environment}'
#     if not os.path.exists(path):
#         raise click.BadParameter(f'Could not locate an .env file at {path}')
#     return environment
