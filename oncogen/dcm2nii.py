"""
In this module an interface to the dcm2nii package is implemented. With this the user can perform translations from dcm 
files to nifti files.

Classes:
    Dcm2niix:       Main interface class. Holds variables for all functionalities of dcm2niix. For options check class
                    documentation.
"""
from helper import mkdir_if_not_exist
from os import sep
from shutil import move

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
