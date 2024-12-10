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

# Main script execution
cd ..
git clone https://github.com/CBICA/BrainMaGe.git
cd BrainMaGe
wget https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_ma.pt 
mv resunet_ma.pt /BrainMaGe/weights/.
wget https://github.com/CBICA/BrainMaGe/raw/master/BrainMaGe/weights/resunet_multi_4.pt
mv resunet_multi_4.pt /BrainMaGe/weights/.

# Create and activate conda environment
sed -i '/=/s/=.*//' environment.yml
sed -i '1s/.*/name: oncogen/' environment.yml
conda env create -f requirements.yml
conda activate OncoGEN

# Get the latest tag and checkout
latesttag=$(git describe --tags)
echo "Checking out ${latesttag}"
git checkout ${latesttag}

# Install the package
python setup.py install
cd .. 

detect_os
install_captk

#cd ..
#git clone https://github.com/antsx/antspy
#cd antspy
#python -m pip install .


