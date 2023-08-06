import logging

from astropy.io import fits
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_math.statistics import average_numpy_arrays

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.visp_base import VispScienceTask


class DarkCalibration(VispScienceTask, QualityMixin):
    """
    Task class for calculation of the averaged dark frame for a VISP calibration run
    """

    def run(self):
        """
        For each beam:
            - Gather input dark frames
            - Calculate master dark
            - Write master dark
            - Record quality metrics

        Returns
        -------
        None

        """
        with self.apm_step(f"Calculating dark frames for {self.num_beams} beams"):
            for beam in range(1, self.num_beams + 1):
                logging.info(f"Gathering input dark frames for beam {beam}")
                input_dark_arrays = self.input_dark_array_generator(beam)
                logging.info(f"Calculating dark for beam {beam}")
                averaged_dark_array = average_numpy_arrays(input_dark_arrays)
                logging.info(f"Writing dark for beam {beam}")
                hdul = fits.HDUList([fits.PrimaryHDU(averaged_dark_array)])
                self.fits_data_write(
                    hdu_list=hdul,
                    tags=[
                        VispTag.intermediate(),
                        VispTag.task("DARK"),
                        VispTag.frame(),
                        VispTag.beam(beam),
                    ],
                )
                # These lines are here to help debugging and can be removed if really necessary
                filename = next(
                    self.read(
                        tags=[
                            VispTag.intermediate(),
                            VispTag.frame(),
                            VispTag.beam(beam),
                            VispTag.task("DARK"),
                        ]
                    )
                )
                logging.info(f"Wrote dark for {beam=} to {filename}")

        with self.apm_step("Finding number of input dark frames"):
            no_of_raw_dark_frames: int = self.count(
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("DARK"),
                ],
            )

        with self.apm_step("Sending dark frame count for quality metric storage"):
            self.quality_store_task_type_counts(
                task_type="dark", total_frames=no_of_raw_dark_frames
            )
