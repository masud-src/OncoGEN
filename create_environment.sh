#!/bin/bash

echo "Download BrainMaGe and create environment"
cd ..
git clone https://github.com/CBICA/BrainMaGe.git
cd BrainMaGe || exit
curl -L -o resunet_ma.pt https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_ma.pt
mv resunet_ma.pt BrainMaGe/weights/.
curl -L -o resunet_multi_4.pt https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_multi_4.pt
mv resunet_multi_4.pt BrainMaGe/weights/.

# Display the options
echo "Please choose an option:"
echo "1) Create anaconda environment according to BrainMaGe README"
echo "2) Create anaconda environment without hard definition of each package"
echo "3) Create custom environment from oncogen.txt (recommended for stand-alone)"
echo "4) Update on OncoFEM installation."

# Read user input
read -p "Enter the number of your choice (1, 2, 3, 4): " choice

# Execute based on user input
case $choice in
    1)
        sed -i '1s/.*/name: oncogen/' environment.yml
        conda env create -f requirements.yml
        ;;
    2)
        sed -i '/=/s/=.*//' environment.yml
        sed -i '1s/.*/name: oncogen/' environment.yml
        conda env create -f requirements.yml
        ;;
    3)
        conda create --name oncogen --file ../OncoGEN/oncogen.txt
        ;;
    4)
        conda init
        conda activate oncofem
        conda install --file ../OncoGEN/oncogen.txt --no-update-deps
        ;;
    *)
        echo "Invalid option. Please choose 1, 2, or 3."
        ;;
esac
cd ..
cd OncoGEN || exit
