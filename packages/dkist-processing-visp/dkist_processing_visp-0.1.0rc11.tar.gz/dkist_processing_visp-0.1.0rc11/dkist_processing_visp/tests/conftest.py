import json
from dataclasses import asdict
from dataclasses import dataclass
from random import choice
from random import randint
from typing import Iterable
from typing import Optional
from typing import Tuple

import numpy as np
import pytest
from astropy.io import fits
from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator import spec122_validator
from dkist_header_validator.translator import sanitize_to_spec214_level1
from dkist_header_validator.translator import translate_spec122_to_spec214_l0
from dkist_processing_common.models.graphql import InputDatasetResponse
from dkist_processing_common.models.graphql import RecipeInstanceResponse
from dkist_processing_common.models.graphql import RecipeRunResponse


class VispHeaders(Spec122Dataset):
    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        time_delta: 10,
        instrument: str = "visp",
        polarimeter_mode: str = "observe_polarimetric",
        **kwargs,
    ):
        super().__init__(
            dataset_shape=dataset_shape,
            array_shape=array_shape,
            time_delta=time_delta,
            instrument=instrument,
            **kwargs,
        )
        self.add_constant_key("WAVELNTH", 656.30)
        self.add_constant_key("VISP_010", 2)
        self.add_constant_key("ID___013", "TEST_PROPOSAL_ID")
        self.add_constant_key("VISP_006", polarimeter_mode)
        self.add_constant_key("PAC__005", "0")
        self.add_constant_key("PAC__007", "10")

    @key_function("VISP_011")
    def date(self, key: str):
        return choice([1, 2])


class VispHeadersValidDarkFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        time_delta: float,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "dark")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("ID___004")


class VispHeadersValidLampGainFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        time_delta: float,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "gain")
        self.add_constant_key("PAC__002", "lamp")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("PAC__003", "on")
        self.add_constant_key("ID___004")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)


class VispHeadersValidSolarGainFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        time_delta: float,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "gain")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("TELSCAN", "Raster")
        self.add_constant_key("ID___004")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)


class VispHeadersValidPolcalFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        time_delta: float,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.add_constant_key("DKIST004", "polcal")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("VISP_019", 1)
        self.add_constant_key("VISP_020", 1)
        self.add_constant_key("TELSCAN", "Raster")
        self.add_constant_key("ID___004")
        self.add_constant_key("PAC__004", "Sapphire Polarizer")
        self.add_constant_key("PAC__005", "60.")
        self.add_constant_key("PAC__006", "clear")
        self.add_constant_key("PAC__007", "0.0")
        self.add_constant_key("PAC__008", "FieldStop (5arcmin)")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)


class VispHeadersValidObserveFrames(VispHeaders):
    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        time_delta: float,
        num_dsps_repeats: int,
        dsps_repeat: int,
        num_raster_steps: int,
        raster_step: int,
        num_modstates: int,
        modstate: int,
        **kwargs,
    ):
        super().__init__(dataset_shape, array_shape, time_delta, **kwargs)
        self.num_dsps_repeats = num_dsps_repeats
        self.num_raster_steps = num_raster_steps
        self.add_constant_key("DKIST004", "observe")
        self.add_constant_key("VISP_019", num_raster_steps)
        self.add_constant_key("VISP_020", raster_step)
        self.add_constant_key("DKIST008", num_dsps_repeats)
        self.add_constant_key("DKIST009", dsps_repeat)
        self.add_constant_key("ID___004")
        self.add_constant_key("VISP_010", num_modstates)
        self.add_constant_key("VISP_011", modstate)


def generate_fits_frame(header_generator: Iterable, shape=None) -> fits.HDUList:
    shape = shape or (1, 10, 10)
    generated_header = next(header_generator)
    translated_header = translate_spec122_to_spec214_l0(generated_header)
    del translated_header["COMMENT"]
    hdu = fits.PrimaryHDU(data=np.ones(shape=shape) * 150, header=fits.Header(translated_header))
    return fits.HDUList([hdu])


def generate_full_visp_fits_frame(
    header_generator: Iterable, data: Optional[np.ndarray] = None
) -> fits.HDUList:
    if data is None:
        data = np.ones(shape=(1, 2000, 2560))
    data[0, 1000:, :] *= np.arange(1000)[:, None][::-1, :]  # Make beam 2 different and flip it
    generated_header = next(header_generator)
    translated_header = translate_spec122_to_spec214_l0(generated_header)
    del translated_header["COMMENT"]
    hdu = fits.PrimaryHDU(data=data, header=fits.Header(translated_header))
    return fits.HDUList([hdu])


def generate_214_l0_fits_frame(
    s122_header: fits.Header, data: Optional[np.ndarray] = None
) -> fits.HDUList:
    """ Convert S122 header into 214 L0 """
    if data is None:
        data = np.ones((1, 10, 10))
    translated_header = translate_spec122_to_spec214_l0(s122_header)
    del translated_header["COMMENT"]
    hdu = fits.PrimaryHDU(data=data, header=fits.Header(translated_header))
    return fits.HDUList([hdu])


def generate_214_l1_fits_frame(
    s122_header: fits.Header, data: Optional[np.ndarray] = None
) -> fits.HDUList:
    """Convert S122 header into 214 L1 only.

    This does NOT include populating all L1 headers, just removing 214 L0 only headers

    NOTE: The stuff you care about will be in hdulist[1]
    """
    l0_s214_hdul = generate_214_l0_fits_frame(s122_header, data)
    l0_header = l0_s214_hdul[0].header
    l0_header["DNAXIS"] = 5
    l0_header["DAAXES"] = 2
    l0_header["DEAXES"] = 3
    l1_header = sanitize_to_spec214_level1(input_headers=l0_header)
    hdu = fits.CompImageHDU(header=l1_header, data=l0_s214_hdul[0].data)

    return fits.HDUList([fits.PrimaryHDU(), hdu])


class Visp122ObserveFrames(VispHeaders):
    def __init__(
        self,
        array_shape: Tuple[int, ...],
        num_steps: int = 4,
        num_exp_per_step: int = 1,
        num_dsps_repeats: int = 5,
    ):
        super().__init__(
            array_shape=array_shape,
            time_delta=10,
            dataset_shape=(num_exp_per_step * num_steps * num_dsps_repeats,) + array_shape[-2:],
        )
        self.add_constant_key("DKIST004", "observe")


class FakeGQLClient:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def execute_gql_query(**kwargs):
        query_base = kwargs["query_base"]

        if query_base == "recipeRuns":
            return [
                RecipeRunResponse(
                    recipeInstanceId=1,
                    recipeInstance=RecipeInstanceResponse(
                        recipeId=1,
                        inputDataset=InputDatasetResponse(
                            inputDatasetId=1,
                            isActive=True,
                            inputDatasetDocument='{"bucket": "bucket-name", "parameters": [{"parameterName": "", "parameterValues": [{"parameterValueId": 1, "parameterValue": "[[1,2,3],[4,5,6],[7,8,9]]", "parameterValueStartDate": "1/1/2000"}]}], "frames": ["objectKey1", "objectKey2", "objectKeyN"]}',
                        ),
                    ),
                )
            ]

    @staticmethod
    def execute_gql_mutation(**kwargs):
        pass


@pytest.fixture()
def recipe_run_id():
    return randint(0, 99999)


@pytest.fixture()
def visp_dataset():
    """
    A header with some common by-frame keywords
    """
    ds = VispHeaders(dataset_shape=(2, 10, 10), array_shape=(1, 10, 10), time_delta=1)
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]

    return header_list[0]


@dataclass
class VispParameters:
    visp_beam_border: int = 1000
    visp_geo_num_otsu: int = 5
    visp_geo_num_theta: int = 1500
    visp_geo_theta_min: float = -np.pi / 90
    visp_geo_theta_max: float = np.pi / 90
    visp_geo_upsample_factor: float = 1000.0
    visp_geo_max_shift: float = 40.0
    visp_geo_poly_fit_order: int = 3
    visp_solar_spectral_avg_window: int = 50
    visp_solar_hairline_fraction: float = 0.8
    visp_solar_zone_prominence: float = 0.2
    visp_solar_zone_width: int = 2
    visp_solar_zone_bg_order: int = 22
    visp_solar_zone_normalization_percentile: float = 99
    visp_solar_zone_rel_height: float = 0.97
    visp_max_cs_step_time_sec: float = 20.0


@pytest.fixture(scope="session")
def input_dataset_document_with_simple_parameters():
    dataset_doc_dict = dict(parameters=[])
    value_id = randint(1000, 2000)
    for pn, pv in asdict(VispParameters()).items():
        values = [
            {
                "parameterValueId": value_id,
                "parameterValue": json.dumps(pv),
                "parameterValueStartDate": "1946-11-20",  # Remember Duane Allman
            }
        ]
        parameter = {"parameterName": pn, "parameterValues": values}
        dataset_doc_dict["parameters"] += [parameter]

    return dataset_doc_dict
