"""
MRI generalisation tutorial

In this tutorial the generalisation process of input dcm files is shown. The MRI scans of the authors brain have been 
made at the Hertie Institute for Clinical Brain Research at the University of Tübingen under the supervision of Dr. 
Justus Marquetand. 
After the definition of the input state, a MRI object is set up. For demonstration, the mri object is initialized 
without a state argument and the state is assigned afterwards manually.
The initial step of every sub-module in OncoFEM is generally done via a setter function, that binds the actual object
to a structural object, i. e. here the generalisation object is attached to the mri object.
The generalisation object holds the following instance variables:
        mri:            Base class is hold for directory information and input for the generalisation,
        work_dir:        String of generalisation outputs,
        study_dir:      String of study direction,
        d2n:            dcm2niix entity is hold which converts DICOM images into Nifti images,
        brain_mage:     BrainMaGe entity which performs the skull stripping,
        gen_shape:      Tuple of integers that represents the general shape of an 3D mri scan.

In general the generalisation process splits into the following steps, that are implemented via distinct methods:

        dcm2niigz:                  Processes a dicom image series into Nifti files and packs it

Possible changes can be done via the 'd2n' object. Herein, the user has the full functionality of the dcm2niix package.
For more information see the documentation of the dcm2niix.py file in the interface sub-package. In general the 
preferences can be set via

mri.generalisation.d2n.a = "n"

        bias_correction:            Performs the bias correction to set every image on the same level of intensity

The bias correction is performed automatically from the ants package, therefore no adjustments can be set. Of course
the user may be free in implementing its own bias correction and may use the already implemented ants package and add
arbitrary setting parameters.

        coregister_modality2atlas:  Coregisters the images into the direction of the SRI24 atlas

The Co-registration is done with CaPT-k. Analogous to the bias correction no adjustments can be set. Again the user can
implement its own by changing the interface. It is automatically chosen between the full modality and modal agnostic
mode.

        skull_strip:                Performs the skull stripping with BrainMaGe

The skull striping is performed with the BrainMaGe package. Similar to bias_correction and co-registration no particular
adjustments can be set and its automatically chosen between the full modality and modal agnostic mode.

        resample2standard:          Resamples the images to a standard resolution

The resampling to standard is done with scikit. It is an additional function that can be used. In the general process
this is already done in co-registration.

        run_all:                    Runs all commands in a clustered command

In order to run the whole process with default preferences the user can chose to run the run_all command.

In the following the t1 and flair modality of the user is generalised either by running the four (dcm2nii, bias 
correction, co-registration and skull stripping) main processes either in separate mode or in the all included run_all
process.
The generated output files can be reviewed in the respective study folder.
"""

########################################################################################################################
# INPUT
import oncogen as og

measure_1 = og.Measure("data/Suditsch/T1", "t1")
measure_2 = og.Measure("data/Suditsch/Flair", "flair")
gen = og.Generalisation()
gen.mri["t1"] = measure_1
gen.mri["flair"] = measure_2
#########################################################################################################################
## GENERALISATION
run_separated = True
if run_separated:
    for measure in {key: value for key, value in gen.mri.items() if value is not None}:
        measure = gen.dcm2niigz(measure)
        measure = gen.bias_correction(measure)

    print("begin coregister")
    gen.coregister_modality2atlas()   
    print("begin skull strip")
    gen.skull_strip()

    #mri.t1_dir = measure_1.dir_act
    #mri.flair_dir = measure_2.dir_act
else:
    gen.run_all()
