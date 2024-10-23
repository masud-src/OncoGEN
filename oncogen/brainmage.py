"""
In this module an interface to the brain mage package is implemented. With this the user can perform skull stripping.

Classes:
    BrainMage:      Main interface class. Holds the dev variable, wherein the modus "cpu" or "gpu" can be chosen with a 
                    string.
"""
import subprocess

class BrainMaGe:
    """
        BrainMage is an advanced skull stripping algorithm designed to accurately and efficiently remove the skull from 
        brain imaging data with tumors, enabling precise analysis and measurement of brain structures.
        Original package can be found here: https://github.com/CBICA/BrainMaGe

        methods:
            init:   initialises with default cpu mode
            single_run: performs a single run with an input file
            multi_4_run: performs a multi 4 run with all gold standard structural images (t1, t1gd, t2, flair)
    """

    def __init__(self):
        self.dev = "cpu"

    def single_run(self, input_file: str, output_file: str, mask_file: str) -> None:
        """
        Performs a single skull stripping run.

        *Arguments*:
            input_file: String of input path
            output_file: String of output path
            mask_file: String of output path for mask file
        *Example*:
            single_run("input_t1.nii.gz", "output_t1.nii.gz", "mask.nii.gz")
        """
        command = ["brain_mage_single_run", "-i", input_file, "-o", output_file, "-m", mask_file, "-dev", self.dev]
        print(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        print(p.communicate())

    def multi_4_run(self, input_files: list, output_file: str) -> None:
        """
        Performs a multi skull stripping run with all gold standard structural MRI scans.

        *Arguments*:
            input_files: List of input files (t1, t1gd, t2, flair)
            output_file: String of output path
        *Example*:
            multi_4_run(["t1.nii.gz", "t1gd.nii.gz", "t2.nii.gz", "flair.nii.gz"], "output_t1.nii.gz")
        """
        command = ["brain_mage_single_run_multi_4", "-i", input_files[0], "-i", input_files[1], "-i", input_files[2], 
                   "-i", input_files[3], "-o", output_file, "-dev", self.dev]
        print(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        print(p.communicate())
