# OncoGEN
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) 

OncoGEN is a **gen**eralisation tool designed to standardise medical images of **onco**logical diseases, enabling 
advanced image processing techniques. In general, the workflow is as follows:
1. Transformation of DICOM image series to NIFTI with dicom2niix [1].
2. Bias correction of the image intensities with the N4 algorithm [2].
3. Co-registration into an atlas with CaPTk [3].
4. Skull stripping with BrainMaGe [4].

* [Software availability](#software)
* [Installation and machine requirements](#installation)
* [Tutorial](#tutorial)
* [How to](#howto)
* [How to cite](#howtocite)
* [Literature](#literature)
* [About](#about)

## <a id="integration"></a> Integration of OncoGEN

OncoFEM is part of a module based umbrella software project for numerical simulations of patient-specific cancer 
diseases, see following figure. From given input states of medical images the disease is modelled and its evolution is 
simulated giving possible predictions. In this way, a digital cancer patient is created, which could be used as a basis 
for further research, as a decision-making tool for doctors in diagnosis and treatment and as an additional illustrative 
demonstrator for enabling patients understand their individual disease. All parts resolve to an open-access framework, 
that is ment to be an accelerator for the digital cancer patient. Each module can be installed and run independently. The 
current state of development comprises the following modules

- OncoFEM (https://github.com/masud-src/OncoFEM)
- OncoGEN (https://github.com/masud-src/OncoGEN)
- OncoTUM (https://github.com/masud-src/OncoTUM)
- OncoSTR (https://github.com/masud-src/OncoSTR)
<p align="center">
 <img src="workflow.png" alt="workflow.png" width="2000"/>
</p>
 
## <a id="software"></a> Software availability

You can either follow the installation instruction below or use the already pre-installed virtual boxes via the 
following Links:

- Version 1.0:  https://doi.org/10.18419/darus-3720

## <a id="installation"></a> Installation and Machine Requirements

There are two different options the installation can be done. First, is the stand-alone installation, where OncoSTR is
simply installed in an Anaconda environment. The other way is to install OncoFEM (https://github.com/masud-src/OncoFEM) 
first and add the missing packets. This installation was tested on a virtual box created with a linux mint 21.2 
cinnamon, 64 bit system and 8 GB RAM on a local machine (intel cpu i7-9700k with 3.6 GHz, 128 GB RAM).

### <a id="standalone"></a> Stand-alone installation

To ensure, the system is ready, it is first updated, upgraded and basic packages are installed via apt.
````bash
sudo apt update
sudo apt upgrade
sudo apt install build-essential python3-pytest gmsh libz-dev git-lfs cmake libeigen3-dev libgmp-dev libmpfr-dev libboost-dev python3-pip git vim
````
```bash
pip install --upgrade pip
pip install numpy==1.22 nipype==1.7.0 filelock==3.0.0 scikit-image==0.16.2 etelemetry==0.2.0 torch vtk fslpy meshio pandas matplotlib nibabel==4.0 dcm2niix tensorboard antspyx==0.4.2
```
- Anaconda needs to be installed. Go to https://anaconda.org/ and follow the installation instructions.
```bash
wget -O Anaconda.sh https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh
bash Anaconda.sh -b -p $HOME/anaconda3
eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
conda init
```
- Run the following command to set up an anaconda environment for OncoGEN and installation on the local system. The
  two big important dependencies are the CaPTk (https://github.com/CBICA/CaPTk) software package and BrainMaGe 
  (https://github.com/CBICA/BrainMaGe)
````bash
git clone https://github.com/masud-src/OncoGEN/
cd OncoGEN
chmod +x install_dependencies.sh
./install_dependencies.sh
````
- Finally install oncostr on the local system.
````bash
python -m pip install --upgrade setuptools
python3 -m pip install .
````
- The package can now be used. To test the correct installation, run a python script with the following code line.
````bash
import oncogen
````

### <a id="oncofem"></a> Install on existing OncoFEM environment

- Run the following command which adds packages to the existing Anaconda environment by pressing 1 in the system dialog.
````bash
git clone https://github.com/masud-src/OncoSTR/
cd OncoSTR
python3 create_conda_environment.py
conda activate oncofem
````
- Finally install oncogen on the local system.
````bash
python3 -m pip install .
````
- The package can now be used. To test the correct installation, run a python script with the following code line.
````bash
import oncogen
````

## <a id="tutorial"></a> Tutorial

There is an tutorial for the umbrella software project provided on DaRUS 
(https://darus.uni-stuttgart.de/dataset.xhtml?persistentId=doi:10.18419/darus-3679). You can download and run the
tutorial_structure_segmentation.py file by run the following lines in your desired directory.
````bash
curl --output tutorial.zip https:/darus.uni-stuttgart.de/api/access/dataset/:persistentId/?persistentId=doi:10.18419/darus-3679
unzip tutorial.zip
tar -xvzf tutorial.tar.gz
rm tutorial.tar.gz tutorial.zip
````

## <a id="howto"></a> How To

You can modify the existing algorithms, respectively expand the existing by your own. Therefore, you can fork and ask 
for pull requests.

## <a id="howtocite"></a> How to cite

TBD

## <a id="literature"></a> Literature

<sup>1</sup> M. Jenkinson, C.F. Beckmann, T.E. Behrens, M.W. Woolrich, S.M. Smith. FSL. NeuroImage, 62:782-90, 2012

## <a id="about"></a> About

OncoSTR is written by Marlon Suditsch
