import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.base import WorkflowDataTaskBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin


class Task(WorkflowDataTaskBase, InputDatasetMixin):
    def run(self):
        pass


INPUT_DATASET = {
    "bucket": "bucket-name",
    "parameters": [
        {
            "parameterName": "param_name",
            "parameterValues": [
                {
                    "parameterValueId": 1,
                    "parameterValue": json.dumps([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                    "parameterValueStartDate": "2000-01-01",
                }
            ],
        }
    ],
    "frames": ["objectKey1", "objectKey2", "objectKeyN"],
}
INPUT_DATASET_PARAMETERS_ONLY_NO_DATE = {
    "parameters": [
        {
            "parameterName": "param_name",
            "parameterValues": [{"parameterValueId": 1, "parameterValue": json.dumps(4)}],
        }
    ]
}

INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES = {
    "parameters": [
        {
            "parameterName": "param_name",
            "parameterValues": [
                {
                    "parameterValueId": 1,
                    "parameterValue": json.dumps(4),
                    "parameterValueStartDate": "2020-03-13",
                },
                {
                    "parameterValueId": 2,
                    "parameterValue": json.dumps(6),
                    "parameterValueStartDate": "1955-01-02",
                },
                {
                    "parameterValueId": 3,
                    "parameterValue": json.dumps(5),
                    "parameterValueStartDate": "2021-12-15",
                },
            ],
        }
    ]
}
INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES_NO_DATE = {
    "parameters": [
        {
            "parameterName": "param_name",
            "parameterValues": [
                {"parameterValueId": 1, "parameterValue": json.dumps(4)},
                {
                    "parameterValueId": 2,
                    "parameterValue": json.dumps(6),
                    "parameterValueStartDate": "1955-01-02",
                },
            ],
        }
    ]
}


@pytest.fixture
def task_with_input_dataset(tmp_path, recipe_run_id):
    def construct_task(input_dataset_dict):
        with Task(
            recipe_run_id=recipe_run_id,
            workflow_name="workflow_name",
            workflow_version="workflow_version",
        ) as task:
            task.scratch = WorkflowFileSystem(
                recipe_run_id=recipe_run_id,
                scratch_base_path=tmp_path,
            )
            task.scratch.workflow_base_path = tmp_path / str(recipe_run_id)
            file_path = task.scratch.workflow_base_path / Path(f"{uuid4().hex[:6]}.ext")
            file_path.write_text(data=json.dumps(input_dataset_dict))
            task.tag(path=file_path, tags=Tag.input_dataset())
            input_dataset_object = json.loads(json.dumps(input_dataset_dict))
            yield task, input_dataset_object
            task.scratch.purge()
            task.constants.purge()

    return construct_task


@pytest.fixture
def multiple_input_datasets(tmp_path, recipe_run_id):
    with Task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.scratch.workflow_base_path = tmp_path / str(recipe_run_id)
        for _ in range(2):
            file_path = task.scratch.workflow_base_path / f"{uuid4().hex[:6]}.ext"
            file_path.write_text(data=json.dumps(INPUT_DATASET))
            task.tag(path=file_path, tags=Tag.input_dataset())
        yield task
        task.scratch.purge()
        task.constants.purge()


def test_input_dataset_document(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: reading the input dataset document
    Then: it matches the string used to create the input dataset
    """
    task, input_dataset_object = next(task_with_input_dataset(INPUT_DATASET))
    task()
    assert task.input_dataset_document == input_dataset_object


def test_multiple_input_datasets(multiple_input_datasets):
    """
    Given: a task with the InputDatasetMixin and multiple tagged input datasets
    When: reading the input dataset document
    Then: an error is raised
    """
    task = multiple_input_datasets
    with pytest.raises(ValueError):
        task.input_dataset_document


def test_no_input_datasets(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: deleting the input dataset tag and then trying to read the input dataset document
    Then: the input dataset document is empty
    """
    task, _ = next(task_with_input_dataset(INPUT_DATASET))
    task.scratch._tag_db.clear_tag(tag=Tag.input_dataset())
    assert task.input_dataset_document == dict()


def test_input_dataset_frames(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: getting the frames in the input dataset
    Then: it matches the frames used to create the input dataset
    """
    task, input_dataset_object = next(task_with_input_dataset(INPUT_DATASET))
    assert task.input_dataset_frames == input_dataset_object.get("frames")


def test_input_dataset_bucket(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: getting the bucket in the input dataset
    Then: it matches the bucket used to create the input dataset
    """
    task, input_dataset_object = next(task_with_input_dataset(INPUT_DATASET))
    assert task.input_dataset_bucket == input_dataset_object.get("bucket")


def test_input_dataset_parameters(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: getting the parameters in the input dataset
    Then: the names of the parameters match the keys in the returned dictionary
    """
    task, input_dataset_object = next(task_with_input_dataset(INPUT_DATASET))
    for key, value in task.input_dataset_parameters.items():
        assert key == input_dataset_object["parameters"][0]["parameterName"]


def test_input_dataset_parameters_get(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: asking for a specific parameter value
    Then: the correct value or default is returned
    """
    task, input_dataset_object = next(task_with_input_dataset(INPUT_DATASET))
    assert task.input_dataset_parameters_get("param_name") == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_input_dataset_parameters_no_key(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: asking for a specific parameter value that does not exist
    Then: a KeyError is raised
    """
    task, input_dataset_object = next(task_with_input_dataset(INPUT_DATASET))
    with pytest.raises(KeyError):
        assert task.input_dataset_parameters_get("not_here")


def test_input_dataset_parameters_get_out_of_range(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin
    When: asking for a specific parameter value at a time that is too far in the past
    Then: an error is raised
    """
    task, input_dataset_object = next(task_with_input_dataset(INPUT_DATASET))
    with pytest.raises(ValueError):
        _ = task.input_dataset_parameters_get("param_name", start_date=datetime(1776, 7, 4))


def test_input_dataset_parameters_get_no_startdate(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin that has a parameter with no start_date
    When: asking for that specific parameter
    Then: the correct value is returned
    """
    task, input_dataset_object = next(
        task_with_input_dataset(INPUT_DATASET_PARAMETERS_ONLY_NO_DATE)
    )
    assert task.input_dataset_parameters_get("param_name") == 4


def test_input_dataset_parameters_multiple_dates(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin that has a parameter with multiple values
    When: asking for that specific parameter
    Then: the correct (i.e., most recent) value is returned
    """
    task, input_dataset_object = next(
        task_with_input_dataset(INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES)
    )
    assert task.input_dataset_parameters_get("param_name", start_date=datetime(2021, 1, 1)) == 4


def test_input_dataset_parameters_multiple_dates_no_startdate(task_with_input_dataset):
    """
    Given: a task with the InputDatasetMixin that has a parameter with multiple values, one of which has no start date
    When: asking for that specific parameter
    Then: the correct value is returned
    """
    task, input_dataset_object = next(
        task_with_input_dataset(INPUT_DATASET_PARAMETERS_ONLY_TWO_VALUES_NO_DATE)
    )
    assert task.input_dataset_parameters_get("param_name") == 6
