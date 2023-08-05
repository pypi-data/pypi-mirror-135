import json
import sys
from pprint import pprint

import pytest

from superwise import Superwise
from superwise.controller.exceptions import *
from superwise.models.model import Model
from superwise.resources.superwise_enums import ModelTypes
from tests import config
from tests import get_sw
from tests import print_results

model_id = None


@pytest.mark.vcr()
def test_create_model_inline():
    sw = get_sw()
    inline_model_test = sw.model.create(Model(name="name", description="this is description", monitor_delay=1))

    print_results("created model object 1", inline_model_test.get_properties())
    assert inline_model_test.name == "name"


@pytest.mark.vcr()
def test_create_model():
    sw = get_sw()
    model = Model()
    global model_id
    model.name = "this is test name"
    model.description = "description"
    model.monitor_delay = 0
    model.ongoing_label = 12
    model.name = "this is test name"
    new_model_model = sw.model.create(model)
    print_results("created task object 2", new_model_model.get_properties())
    assert new_model_model.name == "this is test name"
    assert new_model_model.description == "description"
    task_id = new_model_model.id


@pytest.mark.vcr()
def test_get_models_by_name():
    sw = get_sw()
    global model_id
    print(model_id)
    models = sw.model.get_by_name("Chargeback prediction - task_id 1078")
    print(models)
    assert len(models) == 1
    model_id = models[0].id


@pytest.mark.vcr()
def test_get_model():
    sw = get_sw()
    global model_id
    print(model_id)
    model = sw.model.get_by_id(model_id)
    assert int(model.id) == model_id


@pytest.mark.vcr()
def test_create_incomplete_input():
    sw = get_sw()
    model = Model()
    ok = False
    try:
        ok = True
        model = sw.model.create(model)
    except SuperwiseValidationException as e:
        assert ok == True
        pprint(e)
    print(model.get_properties())

    ok2 = False
    try:
        new_inline = sw.model.create(Model(description="inline model description", monitor_delay=1))
    except SuperwiseValidationException as e:
        pprint(e)
        ok2 = True
    assert ok2 == True
