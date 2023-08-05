import json
import os
import sys
from datetime import datetime
from pprint import pprint

import jwt
import pandas as pd
import pytest
import requests
from google.cloud import storage
from google.oauth2 import service_account
from requests import Response

from project_root import PROJECT_ROOT
from superwise import Client
from superwise import Superwise
from superwise.controller.exceptions import *
from superwise.controller.infer import infer_dtype
from superwise.controller.summary.entities_validator import EntitiesValidationError
from superwise.models.data_entity import DataEntity
from superwise.models.model import Model
from superwise.models.version import Version
from superwise.resources.superwise_enums import DataEntityRole
from superwise.resources.superwise_enums import FeatureType
from superwise.resources.superwise_enums import ModelTypes
from tests import config
from tests import get_entities_fixture
from tests import get_sw


@pytest.fixture(scope="function")
def mock_gcp_client(monkeypatch):
    class GCSClient:
        def __init__(self, *args, **kwargs):
            self.name = "test"

        def bucket(self, bucket_name):
            return GCSClient()

        def blob(self, file_name):
            return GCSClient()

        def download_as_string(self):
            return "asdasdaas"

        def upload_from_string(self, data):
            return None

    monkeypatch.setattr(service_account.Credentials, "from_service_account_info", lambda *args, **kwargs: "")
    monkeypatch.setattr(storage, "Client", lambda *args, **kwargs: GCSClient())


@pytest.fixture(scope="function")
def mock_get_token(monkeypatch):
    monkeypatch.setattr(Client, "get_token", lambda *args, **kwargs: "token")
    monkeypatch.setattr(Client, "get_service_account", lambda *args, **kwargs: {})


@pytest.fixture(scope="function")
def mock_jwt_decode(monkeypatch):
    monkeypatch.setattr(jwt, "decode", lambda *args, **kwargs: {"tenantId": "test"})


@pytest.fixture(scope="function")
def sw(mock_gcp_client, mock_jwt_decode):
    return Superwise(client_id="test", secret="test")


@pytest.fixture(scope="function")
def mock_version_requests(sw, monkeypatch):
    the_response = Response()
    the_response.status_code = 201
    with open(f"{PROJECT_ROOT}/tests/resources/data_entity/assets/entities.json", "r") as fh:
        data_entities = fh.read()
    data_response_response = Response()
    data_response_response._content = data_entities
    data_response_response.status_code = 200
    example_model = Model(name="test", description="test", monitor_delay=1)
    example_version = Version(model_id=1, status="Active", name="test version")

    the_response._content = json.dumps(example_version.get_properties())
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: the_response)
    monkeypatch.setattr(sw.model, "get_by_id", lambda *args, **kwargs: example_model)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: the_response)
    request_get_lambda = lambda url, **kwargs: data_response_response if "data_entities" in url else the_response
    monkeypatch.setattr(requests, "get", request_get_lambda)


def get_entities_fixture(path=f"{PROJECT_ROOT}/tests/resources/basic_schema.json"):
    with open(path, "r") as fh:
        schema = json.loads(fh.read())

    entities = [
        DataEntity(
            dimension_start_ts=m.get("dimension_start_ts", None),
            name=m["name"],
            type=m["type"],
            role=m["role"],
            feature_importance=None,
        )
        for m in schema
    ]
    return entities


def test_dataentity_creation_unit():

    entities = DataEntity(
        dimension_start_ts=None,
        name="barak",
        type=FeatureType.CATEGORICAL,
        role=DataEntityRole.LABEL,
        feature_importance=None,
    )

    assert entities.type == FeatureType.CATEGORICAL.value
    assert entities.role == DataEntityRole.LABEL.value


# source https://stackoverflow.com/questions/32815640/how-to-get-the-difference-between-two-dictionaries-in-python
def diff_dicts(a, b, missing=KeyError):
    """
    Find keys and values which differ from `a` to `b` as a dict.

    If a value differs from `a` to `b` then the value in the returned dict will
    be: `(a_value, b_value)`. If either is missing then the token from
    `missing` will be used instead.

    :param a: The from dict
    :param b: The to dict
    :param missing: A token used to indicate the dict did not include this key
    :return: A dict of keys to tuples with the matching value from a and b
    """
    return {key: (a.get(key, missing), b.get(key, missing)) for key in dict(set(a.items()) ^ set(b.items())).keys()}


def test_infer_dtypes(mock_get_token, sw, mock_version_requests):
    df = pd.read_json(f"{PROJECT_ROOT}/tests/resources/internal_sdk/data_bool.json")
    expected_infer_path = f"{PROJECT_ROOT}/tests/resources/data_entity/expected_infer.json"
    with open(expected_infer_path) as f:
        expected_infer = json.load(f)

    dtypes_infered = infer_dtype(df)
    try:
        assert dtypes_infered == expected_infer
    except:
        diff = diff_dicts(expected_infer, dtypes_infered)
        print(diff)
        raise Exception("infered datatypes not same as schema")


def test_create_version(mock_get_token, sw, mock_version_requests):
    # entities = get_entities_fixture()
    df = pd.read_json(f"{PROJECT_ROOT}/tests/resources/internal_sdk/data_bool.json")
    schema_path = f"{PROJECT_ROOT}/tests/resources/internal_sdk/basic_schema.json"
    with open(schema_path) as f:
        schema = json.load(f)

    roles = {}
    dtypes = {}
    for entity in schema:
        if entity["role"] != "feature":
            roles[entity["name"]] = entity["role"]
        dtypes[entity["name"]] = entity["type"]

    # Example of dtypes
    # dtypes = {
    #     "f0": "Numeric",
    #     "binary_bool_full": "Boolean",
    #     "binary_float_full": "Categorical",
    #     "ts": "Timestamp",
    #     "record_id": "Categorical",
    # }

    # Example of roles
    # roles = {
    #     "f0": "feature",
    #     "binary_bool_full": "feature",
    #     "binary_float_full": "feature",
    #     "ts": "time stamp",
    #     "record_id": "id",
    # }

    entities = sw.data_entity.summarise(
        data=df,
        entities_dtypes=dtypes,
        specific_roles=roles,
        default_role="feature",
        importance=False,
        importance_target_label=None,
        importance_sample=None,
        base_version=None,
    )
    version_external = Version(model_id=1, name="test version", data_entities=entities)
    model = sw.version.create(version_external, wait_until_complete=False)
    assert isinstance(model, Version)

    ## create a new one, but now with infer datatype
    entities = sw.data_entity.summarise(
        data=df,
        entities_dtypes=None,
        specific_roles=roles,
        default_role="feature",
        importance=False,
        importance_target_label=None,
        importance_sample=None,
        base_version=None,
    )
    version_external_2 = Version(model_id=1, name="test version with infer dtypes", data_entities=entities)
    model_2 = sw.version.create(version_external, wait_until_complete=False)
    assert isinstance(model_2, Version)


def test_create_base_version(mock_get_token, sw, mock_version_requests):

    df = pd.read_json(f"{PROJECT_ROOT}/tests/resources/internal_sdk/data_bool.json")
    schema_path = f"{PROJECT_ROOT}/tests/resources/internal_sdk/basic_schema.json"
    with open(schema_path) as f:
        schema = json.load(f)

    df = df.rename(columns={"f31": "f31_change"})

    roles = {}
    dtypes = {}
    for entity in schema:
        if entity["name"] == "f31":
            entity["name"] = "f31_change"
        if entity["role"] != "feature":
            roles[entity["name"]] = entity["role"]
        dtypes[entity["name"]] = entity["type"]

    base_version = Version(id=1, status="Active")

    entities = sw.data_entity.summarise(
        data=df,
        entities_dtypes=dtypes,
        specific_roles=roles,
        default_role="feature",
        importance_target_label=None,
        importance_sample=None,
        base_version=base_version,
    )
    version_external = Version(model_id=1, name="test version", data_entities=entities)
    model = sw.version.create(version_external, wait_until_complete=False)
    assert isinstance(model, Version)
    print(model.get_properties())


def test_get_version(mock_get_token, sw, mock_version_requests):
    version = sw.version.get_by_id(1)
    assert isinstance(version, Version)


def test_get_version_data_entities(mock_get_token, sw, mock_version_requests):
    data_entities = sw.version.get_data_entities(version_id=1)
    assert isinstance(data_entities, list)
    assert isinstance(data_entities[0], DataEntity)
