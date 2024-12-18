#!/bin/bash

pip install --upgrade pip
pip install numpy==1.23.5
pip install nipype==1.7.0 filelock==3.0.0 scikit-image==0.16.2 etelemetry==0.2.0 torch==1.11 nibabel==4.0 dcm2niix tensorboard antspyx==0.4.2

cd ..
cd BrainMaGe || exit
latesttag=$(git describe --tags)
echo "Checking out ${latesttag}"
git checkout ${latesttag}
python setup.py install
echo "BrainMaGe installation successful"
cd ..
cd OncoGEN || exit
echo "Installation of prerequisites is completed successfully!"
echo "Some changes require the terminal to be restarted."
echo "Please close and reopen your terminal to apply the changes."
exit 0