import json
from datetime import datetime

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.tags import Tag

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.lamp import LampCalibration
from dkist_processing_visp.tests.conftest import FakeGQLClient
from dkist_processing_visp.tests.conftest import generate_fits_frame
from dkist_processing_visp.tests.conftest import VispHeadersValidLampGainFrames

RNG = np.random.default_rng()


@pytest.fixture(scope="function")
def lamp_calibration_task(tmp_path, recipe_run_id, input_dataset_document_with_simple_parameters):
    number_of_modstates = 2
    number_of_beams = 2
    with LampCalibration(
        recipe_run_id=recipe_run_id, workflow_name="lamp_gain_calibration", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        doc_path = task.scratch.workflow_base_path / "dataset_doc.json"
        with open(doc_path, "w") as f:
            f.write(json.dumps(input_dataset_document_with_simple_parameters))
        task.tag(doc_path, VispTag.input_dataset())
        task.constants[BudName.num_modstates.value] = number_of_modstates

        start_time = datetime.now()
        for j in range(number_of_beams):
            # Make intermediate dark frame
            dark_cal = RNG.standard_normal((10, 10))
            dark_hdul = fits.HDUList([fits.PrimaryHDU(data=dark_cal)])
            task.fits_data_write(
                hdu_list=dark_hdul,
                tags=[
                    VispTag.intermediate(),
                    VispTag.frame(),
                    VispTag.task("DARK"),
                    VispTag.beam(j + 1),
                ],
            )
            for i in range(number_of_modstates):
                ds = VispHeadersValidLampGainFrames(
                    dataset_shape=(number_of_modstates, 10, 10),
                    array_shape=(1, 10, 10),
                    time_delta=10,
                    num_modstates=number_of_modstates,
                    modstate=i + 1,
                    start_time=start_time,
                )
                header_generator = (
                    spec122_validator.validate_and_translate_to_214_l0(
                        d.header(), return_type=fits.HDUList
                    )[0].header
                    for d in ds
                )
                hdul = generate_fits_frame(header_generator=header_generator)
                task.fits_data_write(
                    hdu_list=hdul,
                    tags=[
                        VispTag.input(),
                        VispTag.task("LAMP_GAIN"),
                        VispTag.modstate(i + 1),
                        VispTag.frame(),
                        VispTag.beam(j + 1),
                    ],
                )
        yield task, number_of_modstates, number_of_beams
        task.scratch.purge()
        task.constants.purge()


def test_lamp_calibration_task(lamp_calibration_task, mocker):
    """
    Given: A LampCalibration task
    When: Calling the task instance
    Then: The correct number of output lamp gain frames exists, and are tagged correctly
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    # When
    task, number_of_modstates, number_of_beams = lamp_calibration_task
    task()
    # Then
    tags = [
        VispTag.task("LAMP_GAIN"),
        VispTag.intermediate(),
    ]
    assert len(list(task.read(tags=tags))) == number_of_modstates * number_of_beams

    for i in range(number_of_modstates):
        for j in range(number_of_beams):
            tags = [
                VispTag.task("LAMP_GAIN"),
                VispTag.intermediate(),
                VispTag.modstate(i + 1),
                VispTag.beam(j + 1),
            ]
            assert len(list(task.read(tags=tags))) == 1

    tags = [
        VispTag.task("LAMP_GAIN"),
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
                tags=[VispTag.input(), VispTag.frame(), VispTag.task("LAMP_GAIN")]
            )
