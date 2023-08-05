import json

import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.dark import DarkCalibration
from dkist_processing_visp.tests.conftest import FakeGQLClient
from dkist_processing_visp.tests.conftest import generate_fits_frame
from dkist_processing_visp.tests.conftest import VispHeadersValidDarkFrames


@pytest.fixture(scope="function")
def dark_calibration_task(tmp_path, recipe_run_id):
    with DarkCalibration(
        recipe_run_id=recipe_run_id, workflow_name="dark_calibration", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        ds = VispHeadersValidDarkFrames(
            dataset_shape=(5, 512, 512), array_shape=(1, 512, 512), time_delta=10
        )
        header_generator = (
            spec122_validator.validate_and_translate_to_214_l0(
                d.header(), return_type=fits.HDUList
            )[0].header
            for d in ds
        )
        for i in range(3):
            hdul = generate_fits_frame(header_generator=header_generator)
            task.fits_data_write(
                hdu_list=hdul,
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("DARK"),
                    VispTag.beam(1),
                ],
            )
        for i in range(2):
            hdul = generate_fits_frame(header_generator=header_generator)
            task.fits_data_write(
                hdu_list=hdul,
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("DARK"),
                    VispTag.beam(2),
                ],
            )
        yield task
        task.scratch.purge()
        task.constants.purge()


def test_dark_calibration_task(dark_calibration_task, mocker):
    """
    Given: A DarkCalibration task
    When: Calling the task instance
    Then: Only one average intermediate dark frame exists
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task = dark_calibration_task
    task()
    # Then
    tags = [
        VispTag.task("DARK"),
        VispTag.intermediate(),
        VispTag.beam(1),
    ]
    assert len(list(task.read(tags=tags))) == 1

    tags = [
        VispTag.task("DARK"),
        VispTag.intermediate(),
        VispTag.beam(2),
    ]
    assert len(list(task.read(tags=tags))) == 1

    tags = [
        VispTag.task("DARK"),
        VispTag.intermediate(),
    ]
    for filepath in task.read(tags=tags):
        assert filepath.exists()

    quality_files = task.read(tags=[Tag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.count(
                tags=[VispTag.input(), VispTag.frame(), VispTag.task("DARK")]
            )
