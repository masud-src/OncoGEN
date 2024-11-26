import os
from pathlib import Path
from typing import Tuple
import subprocess
from os import sep
from shutil import move
import dcm2niix as d2n


class Measure:
    """
    A measure is the actual measure of a mri modality. It usually comes raw in dicom format. In order to pre-process
    there are particular arguments for the conversion into nifti format (dir_ngz), for bias correction (dir_bia), for
    co-registration (dir_cor) and the skull stripped version (dir_sks).

    *Attributes*:
        dir_src:          Directory of original input on hard disc
        dir_act:          Directory of actual processing step of the image
        dir_ngz:          Directory of nifti converted image
        dir_bia:          Directory of bias corrected image
        dir_cor:          Directory of co-registered image
        dir_sks:          Directory of skull stripped image
        dir_brainmask:    Directory of brain mask
        state_id:         String of state identification
        subj_id:          String of subject of measure
        study_dir:        String of study directory
        date:             Time stamp of measure
        modality:         String, identifier of modality (t1, t1gd, t2, flair, seg)
    """
    def __init__(self, path: str, modality: str):
        self.dir_src = path
        self.dir_act = path
        self.dir_ngz = None
        self.dir_bia = None
        self.dir_cor = None
        self.dir_sks = None
        self.dir_brainmask = None
        self.state_id = None
        self.subj_id = None
        self.study_dir = None
        self.date = None
        self.modality = modality


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


class Dcm2niix:
    """
    Chris Rorden's dcm2niiX version v1.0.20211006  GCC9.4.0 x86-64 (64-bit Linux)
    Options :
        -1..-9 : gz compression level (1=fastest..9=smallest, default 6)
        -a : adjacent DICOMs (images from same series always in same folder) for faster conversion (n/y, default n)
        -b : BIDS sidecar (y/n/o [o=only: no NIfTI], default y)
        -ba : anonymize BIDS (y/n, default y)
        -c : comment stored in NIfTI aux_file (provide up to 24 characters e.g. '-c first_visit')
        -d : directory search depth. Convert DICOMs in sub-folders of in_folder? (0..9, default 5)
        -e : export as NRRD (y) or MGH (o) instead of NIfTI (y/n/o, default n)
        -f : filename (%a=antenna (coil) name, %b=basename, %c=comments, %d=description, %e=echo number, %f=folder name, %g=accession number, %i=ID of patient, %j=seriesInstanceUID, %k=studyInstanceUID, %m=manufacturer, %n=name of patient, %o=mediaObjectInstanceUID, %p=protocol, %r=instance number, %s=series number, %t=time, %u=acquisition number, %v=vendor, %x=study ID; %z=sequence name; default '%f_%p_%t_%s')
        -g : generate defaults file (y/n/o/i [o=only: reset and write defaults; i=ignore: reset defaults], default n)
        -h : show help
        -i : ignore derived, localizer and 2D images (y/n, default n)
        -l : losslessly scale 16-bit integers to use dynamic range (y/n/o [yes=scale, no=no, but uint16->int16, o=original], default o)
        -m : merge 2D slices from same series regardless of echo, exposure, etc. (n/y or 0/1/2, default 2) [no, yes, auto]
        -n : only convert this series CRC number - can be used up to 16 times (default convert all)
        -o : output directory (omit to save to input folder)
        -p : Philips precise float (not display) scaling (y/n, default y)
        -r : rename instead of convert DICOMs (y/n, default n)
        -s : single file mode, do not convert other images in folder (y/n, default n)
        -u : up-to-date check
        -v : verbose (n/y or 0/1/2, default 0) [no, yes, logorrheic]
        -w : write behavior for name conflicts (0,1,2, default 2: 0=skip duplicates, 1=overwrite, 2=add suffix)
        -x : crop 3D acquisitions (y/n/i, default n, use 'i'gnore to neither crop nor rotate 3D acquistions)
        -z : gz compress images (y/o/i/n/3, default n) [y=pigz, o=optimal pigz, i=internal:miniz, n=no, 3=no,3D]
        --big-endian : byte order (y/n/o, default o) [y=big-end, n=little-end, o=optimal/native]
        --progress : Slicer format progress information (y/n, default n)
        --ignore_trigger_times : disregard values in 0018,1060 and 0020,9153
        --terse : omit filename post-fixes (can cause overwrites)
        --version : report version
        --xml : Slicer format features
    Examples :
        dcm2niix /Users/chris/dir
        dcm2niix -c "my comment" /Users/chris/dir
        dcm2niix -o /users/cr/outdir/ -z y ~/dicomdir
        dcm2niix -f %p_%s -b y -ba n ~/dicomdir
        dcm2niix -f mystudy%s ~/dicomdir
        dcm2niix -o "~/dir with spaces/dir" ~/dicomdir
        Example output filename: 'myFolder_MPRAGE_19770703150928_1.nii'
    """

    def __init__(self):
        self.compress = "6"
        self.a = "n"
        self.b = "n"
        self.ba = "y"
        self.d = "5"
        self.e = "n"
        self.f = "%f_%p_%t_%s"
        self.g = "n"
        self.i = "n"
        self.l = "o"
        self.m = "2"
        self.n = None
        self.o = None
        self.s = "n"
        self.u = None
        self.v = "0"
        self.w = "2"
        self.x = "n"
        self.z = "y"
        self.extra = None
        self.print_command = False

    def run_dcm2niix(self, input_directory:str, output_directory:str) -> str:
        """
        Runs dcm2niix command with presetted configurations in dcm2niix entity.

        *Arguments:*
            input_directory: String, directory of files
            output_directory: String, directory for saved output file

        *Example:*
            file_path = un_dcm2niix(input_directory, output_directory)
        """
        command = ["-" + self.compress + " " if self.compress is not None else ""]
        command.append("-a ")
        command.append(self.a)
        command.append("-b")
        command.append(self.b)
        command.append("-ba")
        command.append(self.ba)
        command.append("-d")
        command.append(self.d)
        command.append("-e")
        command.append(self.e)
        command.append("-f")
        command.append(self.f)
        command.append("-g")
        command.append(self.g)
        command.append("-i")
        command.append(self.i)
        command.append("-l")
        command.append(self.l)
        command.append("-m")
        command.append(self.m)
        command.append("-" + self.n + " " if self.n is not None else "")
        command.append("-" + self.o + " " if self.o is not None else "")
        command.append("-s")
        command.append(self.s)
        command.append("-z")
        command.append(self.z)
        command.append("-" + self.u + " " if self.u is not None else "")
        command.append(self.extra if self.extra is not None else "")
        command.append(input_directory)

        if self.print_command:
            print(command)

        d2n.main(command)
        mkdir_if_not_exist(output_directory)
        move(input_directory + sep + self.f + ".nii.gz", output_directory + self.f + ".nii.gz")
        return output_directory + self.f + ".nii.gz"


def split_path(s: str) -> Tuple[str, str]:
    """
    Splits Filepath into file and path

    *Arguments:*
        s: String

    *Example:*
        file, path = splitPath(s) 
    """
    import os
    f = os.path.basename(s)
    p = s[:-(len(f))-1]
    return str(f), str(p)

def mkdir_if_not_exist(directory: str) -> str:
    """
    Makes directory if not exists and returns the string

    *Arguments*:
        dir: String

    *Example*:
        dir = mkdir_if_not_exist(dir) 
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def get_path_file_extension(input_file: str) -> Tuple[str, str, str]:
    """ 
    Returns path, the filename and the filename without extension.

    *Arguments:*
        input_file: String

    *Example:*
        path, file, file_wo_extension = get_path_file_extension(input_file)
    """
    file, path = split_path(input_file)
    file_wo_extension = Path(Path(input_file).stem).stem
    return path, file, file_wo_extension
