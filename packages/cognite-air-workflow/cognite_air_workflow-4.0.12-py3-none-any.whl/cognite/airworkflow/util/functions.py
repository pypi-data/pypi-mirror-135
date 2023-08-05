import os
import time
from pathlib import Path
from typing import Dict, Iterator, Optional, Union

from cognite.client.exceptions import CogniteAPIError
from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Function
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError, ReadTimeoutError

import cognite.airworkflow.constants as constants
from cognite.airworkflow.util import cdf, env

CHANNEL = "model_deployment_fails"


def format_secret_names(secrets: Dict[str, str]) -> Dict[str, str]:
    new_secrets = {}
    for key, item in secrets.items():
        new_key = key.lower().replace("_", "-")
        new_secrets[new_key] = item

    return new_secrets


def delete_function_if_exists(
    client: CogniteClient,
    function_name: Optional[str] = None,
    function_id: Optional[int] = None,
):
    assert function_name is not None or function_id is not None

    if cdf.does_function_exist(client, function_name, function_id):
        print(
            f"Function with name/id {function_name if function_id is None else function_id} "
            + f"already exists for {client.config.project}, will delete it.",
            flush=True,
        )
        if function_id:
            client.functions.delete(id=function_id)
        if function_name:
            client.functions.delete(external_id=function_name)


def deploy_function(
    client: CogniteClient,
    function_name: str,
    file_id: int,
    secrets: Dict[str, str],
    owner: str = "",
    oidc: bool = True,
) -> None:
    delete_function_if_exists(client, function_name)
    secrets = format_secret_names(secrets)
    if len(secrets) > 5:
        raise ValueError("Not more than 5 secrets allowed.")
    for secret in secrets.keys():
        if len(secret) > 15:
            raise ValueError(f"Secret name is too long (15 characters max): {secret}")
    print("Deploying function ...", flush=True)
    x = 0
    y = 0
    while x < 3:
        function = None
        try:
            if oidc:
                print(
                    f"Creating function using OIDC for function :{function_name} in project :{client.config.project}."
                )
            else:
                print(
                    f"Creating function using API key for function :{function_name} in project {client.config.project}"
                )
            function = client.functions.create(
                name=function_name,
                file_id=file_id,
                secrets=secrets,
                external_id=function_name,
                api_key=client._config.api_key if not oidc else None,
                owner=owner,
            )
            success, function_object = cdf.await_function_deployment(client, function, 900)
            if not success:
                if function_object is not None:
                    print(f"Error while deploying function {function_name} and function_id :{function_object.id}")
                    print(f"Error message :{function_object.error.message}")
                    print(f"Error stack trace :{function_object.error.trace}")
                raise TimeoutError(f"Deployment of function with external id {function_name} timed out or failed.")

            print(
                f"Function {function_name} (id: {function.id}) "
                + f"successfully created in project {client.config.project}.",
                flush=True,
            )
            x = 3
        except (
            TimeoutError,
            ReadTimeoutError,
            CogniteAPIError,
            MaxRetryError,
            ConnectionError,
            AttributeError,
        ) as e:
            print(e, flush=True)
            if isinstance(e, CogniteAPIError) and e.code == 400:
                time.sleep(1)
                if function is not None:
                    delete_function_if_exists(client, function_id=function.id)
                else:
                    delete_function_if_exists(client, function_name=function_name)
                y += 1
                if y > 30:
                    x += 1
                    y = 0
            else:
                x += 1
            if x >= 3:
                raise TimeoutError("Tried to deploy three times and failed.")


def delete_function(client: CogniteClient, external_id: str):
    if cdf.does_function_exist(client, external_id):
        print(f"Deleting function named {external_id} ...", flush=True)
        client.functions.delete(external_id=external_id)
        print(f"Function {external_id} successfully deleted from project {client.config.project}.", flush=True)


def list_dangling_function(
    client: CogniteClient,
    expected_functions: Iterator[str],
    *,
    name_prefix: str = "",
) -> Iterator[Function]:
    functions = client.functions.list()
    if name_prefix:
        functions = list(filter(lambda f: name_prefix in f.name, functions))
    return filter(lambda f: f.name not in expected_functions, functions)


def get_function_name(
    path: Union[Path, str],
    *,
    version: str = "",
    ref: str = "",
    pr: bool = False,
    latest: bool = False,
) -> str:
    if isinstance(path, str):
        path = Path(path)
    if os.getenv(constants.gitlab_ci_project):
        function_name = f"{os.environ[constants.gitlab_ci_project]}/{path.name}:"
    else:
        function_name = f"{env.get_repo_name_auto()}/{path.name}:"
    if latest:
        return f"{function_name}latest"
    elif pr:
        if os.getenv(constants.gitlab_function_name_addition):
            return f"{function_name}{ref if ref else env.get_env_value(constants.gitlab_function_name_addition)}"

        else:
            return f"{function_name}{ref if ref else env.get_env_value('GITHUB_HEAD_REF')}"
    return f"{function_name}{version}"


def get_relative_function_path(path: Path) -> str:
    return "/".join(path.parts[path.parts.index("functions") + 1 :])  # noqa
