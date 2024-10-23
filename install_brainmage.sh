#!/bin/bash

cd ..
git clone https://github.com/CBICA/BrainMaGe.git
cd BrainMaGe
wget https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_ma.pt ./BrainMaGe/weights
wget https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_multi_4.pt ./BrainMaGe/weights

# Create and activate conda environment
conda env create -f requirements.yml -n OncoGEN
conda activate OncoGEN

# Get the latest tag and checkout
latesttag=$(git describe --tags)
echo "Checking out ${latesttag}"
git checkout ${latesttag}

# Install the package
python setup.py install
cd ../OncoGEN

