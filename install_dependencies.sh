#!/bin/bash

# Function to detect the operating system
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="macOS";;
        CYGWIN*|MINGW*|MSYS*) OS="Windows";;
        *)          OS="Unknown";;
    esac
}

# Function to download and install the appropriate file
install_captk() {
    case $OS in
        Linux)
            URL="https://captk.projects.nitrc.org/CaPTk_1.8.1_Installer.bin"
            FILENAME="CaPTk_Installer.bin"
            ;;
        macOS)
            URL="https://captk.projects.nitrc.org/CaPTk_1.8.1_Installer.pkg"
            FILENAME="CaPTk_Installer.pkg"
            ;;
        Windows)
            URL="https://captk.projects.nitrc.org/CaPTk_1.8.1_Installer.exe"
            FILENAME="CaPTk_Installer.exe"
            ;;
        *)
            echo "Unsupported operating system: $OS"
            exit 1
            ;;
    esac

    echo "Detected OS: $OS"
    echo "Downloading from $URL..."

    # Download the file
    wget -O "$FILENAME" "$URL"

    # Install based on the OS
    if [[ $OS == "Linux" ]]; then
        chmod +x "$FILENAME"
        ./"$FILENAME"
    elif [[ $OS == "macOS" ]]; then
        sudo installer -pkg "$FILENAME" -target /
    elif [[ $OS == "Windows" ]]; then
        echo "Run the installer manually: $FILENAME"
    fi

    echo "Installation complete."
}

echo "Installation of BrainMaGe"
cd ..
git clone https://github.com/CBICA/BrainMaGe.git
cd BrainMaGe || exit
wget https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_ma.pt
mv resunet_ma.pt /BrainMaGe/weights/.
wget https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_multi_4.pt
mv resunet_multi_4.pt /BrainMaGe/weights/.

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
        conda activate oncofem
        conda install --file ../OncoGEN/oncogen.txt --no-update-deps
        ;;
    *)
        echo "Invalid option. Please choose 1, 2, or 3."
        ;;
esac

conda activate oncogen

pip install --upgrade pip
pip install numpy==1.22
pip nipype==1.7.0 filelock==3.0.0 scikit-image==0.16.2 etelemetry==0.2.0 torch=1.11 nibabel==4.0 dcm2niix tensorboard antspyx==0.4.2

latesttag=$(git describe --tags)
echo "Checking out ${latesttag}"
git checkout ${latesttag}
python setup.py install
cd .. 

echo "Installation of CaPTk"
detect_os
install_captk
