"""
Generalisation of the input files for further processing of the segmentations.

Classes:
    Generalisation:     Holds all information and is the entry point for every process done. Each process can be
                        perfomed solitary or everything is done in a clustered run command.
"""
import os
import subprocess
from .utils import Measure, Dcm2niix, BrainMaGe, mkdir_if_not_exist, get_path_file_extension
import ants

GENERALISATION_PATH = "generalisation" + os.path.sep
SRI24_T1 = "data/sri24/templates/T1_brain.nii"
SRI24_T2 = "data/sri24/templates/T2_brain.nii"
CAPTK_DIR = "/home/marlon/Software/CaPTk/1.8.1/captk"


class Generalisation:
    """
    The generalisation entity is the entry point of patient-specific magnetic resonance image series. Herein, the 
    images are set into a comparable scope for further investigations.

    *Arguments*:
        mri:            Base class is hold for directory information
        work_dir:        String of generalisation outputs
        study_dir:      String of study direction
        d2n:            dcm2niix entity is hold which converts DICOM images into Nifti images
        brain_mage:     BrainMaGe entity which performs the skull stripping
        gen_shape:      Tuple of integers that represents the general shape of an 3D mri scan.

    *Methods*:
        dcm2niigz:                  Processes a dicom image series into Nifti files and packs it
        bias_correction:            Performs the bias correction to set every image on the same level of intensity
        coregister_modality2atlas:  Coregisters the images into the direction of the SRI24 atlas
        skull_strip:                Performs the skull stripping with BrainMaGe
        run_all:                    Runs all commands in a clustered command
    """

    def __init__(self, work_dir: str = None):
        if work_dir is None:
            work_dir = os.getcwd() + os.sep
        if not work_dir.endswith(os.sep):
            work_dir = work_dir + os.sep
        self.work_dir = work_dir
        self.gen_shape = (240, 240, 155)
        self.d2n = None
        self.mri = {"t1": None, "t1ce": None, "t2": None, "flair": None}
        self.full_ana_modality = False
        self.brain_mage = BrainMaGe()

    def set_work_dir(self, work_dir: str):
        """
        sets the working directory of the generalisation.

        :param work_dir: String of the working directory, this is where the output is put
        :return: 
        """
        self.work_dir = work_dir

    def dcm2niigz(self, measure: Measure) -> Measure:
        """
        converts input dcm file (folder) into packed nifti file

        # Arguments:
            measure: Measure contains all neccesary data
        """
        mkdir_if_not_exist(self.work_dir)
        dcm_dir = measure.dir_src
        niigz_dir = self.work_dir
        self.d2n = Dcm2niix()
        self.d2n.f = measure.modality
        measure.dir_ngz = self.d2n.run_dcm2niix(dcm_dir, niigz_dir)
        measure.dir_act = measure.dir_ngz
        return measure

    def bias_correction(self, measure: Measure) -> Measure:
        """
        Bias correction of the images

        *Arguments*:
            measure: Measure contains all necessary data
        """
        mkdir_if_not_exist(self.work_dir)
        input_image = measure.dir_act
        measure.dir_bia = measure.dir_ngz.replace('.nii', '_bc.nii')
        measure.dir_act = measure.dir_bia
        image = ants.image_read(input_image)
        image_n4 = ants.n4_bias_field_correction(image)
        ants.image_write(image_n4, measure.dir_bia)
        return measure

    def coregister_modality2atlas(self) -> None:
        """
        Co-registers different modalities into the same space. This should be done into a general atlas space
        """
        mkdir_if_not_exist(self.work_dir)
        modalities = {"t1": "-t1", "t1ce": "-t1c", "t2": "-t2", "flair": "-fl"}
        self.full_ana_modality = all(value is not None for value in self.mri.values())
        if self.full_ana_modality:
            command = [CAPTK_DIR]
            command.append("BraTSPipeline.cwl")
            for measure in {key: value for key, value in self.mri.items() if value is not None}.values():
                input_path = measure
                measure.dir_cor = self.work_dir + str(measure.modality) + "_to_sri.nii.gz"
                measure.dir_act = measure.dir_cor
                command.append(modalities[measure.modality])
                command.append(input_path)

            command.append("-o")
            command.append(self.work_dir)
            command.append("-s")
            command.append("0")
            command.append("-b")
            command.append("0")
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            print(p.communicate())

        else:
            for measure in {key: value for key, value in self.mri.items() if value is not None}.values():
                input_dir = measure.dir_bia
                path, file, file_wo_extension = get_path_file_extension(input_dir)
                file_sri24 = file_wo_extension + "_to_SRI.nii.gz"
                measure.dir_act = self.work_dir + file_sri24
                command = [CAPTK_DIR]
                command.append("Preprocessing.cwl")
                command.append("-i")
                command.append(input_dir)
                command.append("-rFI")
                if measure.modality == "t2":
                    command.append(SRI24_T2)
                else:
                    command.append(SRI24_T1)
                command.append("-o")
                command.append(self.work_dir + file_sri24)
                command.append("-reg")
                command.append("RIGID")
                p = subprocess.Popen(command, stdout=subprocess.PIPE)
                print(p.communicate())

    def skull_strip(self) -> None:
        """
        Skull strips the given input images
        """
        mkdir_if_not_exist(self.work_dir)
        self.full_ana_modality = all(value is not None for value in self.mri.values())
        if self.full_ana_modality:
            input_files = [self.mri["t1"], self.mri["t2"], self.mri["t1ce"], self.mri["flair"]]
            output_dir = self.work_dir + os.sep
            self.brain_mage.multi_4_run(input_files, output_dir)

        else:
            for measure in {key: value for key, value in self.mri.items() if value is not None}.values():
                path, file, file_wo_extension = get_path_file_extension(measure.dir_act)
                measure.dir_sks = self.work_dir + file_wo_extension + "_sks.nii.gz"
                measure.dir_brainmask = self.work_dir + file_wo_extension + "_brain.nii.gz"
                self.brain_mage.single_run(measure.dir_act, measure.dir_sks, measure.dir_brainmask)
                measure.dir_act = measure.dir_brainmask

    def run_all(self) -> None:
        """
        Runs gen process:
            1. dcm2niigz
            2. Bias Correction (N4)
            3. Co-register axial, sagittal, coronal into one image (not implemented)
            4. Co-register into Atlas Space
            5. Skull strip 
            6. Resample onto Standard sample size
        """
        print("Begin generalisation")
        self.full_ana_modality = all(value is not None for value in self.mri.values())
        print("Full anatomical model: ", str(self.full_ana_modality))

        print("Begin dcm2niigz + bias correction")
        for measure in {key: value for key, value in self.mri.items() if value is not None}.values():
            self.dcm2niigz(measure)
            self.bias_correction(measure)

        print("Begin coregister 2 atlas")
        self.coregister_modality2atlas()

        print("Begin skull strip")
        self.skull_strip()
