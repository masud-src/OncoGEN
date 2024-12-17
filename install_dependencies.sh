#!/bin/bash

echo "Choose the environment: (1) for OncoFEM, (2) for just pip installation"
read env_choice

if [[ "$env_choice" == "1" ]]; then
  conda activate oncofem
elif [[ "$env_choice" == "2" ]]; then
  echo "only pip installation is chosen."
else
  echo "Invalid choice. Please choose either '1' for OncoSTR or '2' for OncoFEM."
  exit 1
fi

# Function to install packages for Linux
install_linux() {
    echo "Detected Linux OS. Proceeding with installation."
    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y build-essential python3-pytest libz-dev cmake libeigen3-dev libgmp-dev libgmp3-dev libmpfr-dev libboost-all-dev python3-pip
}

# Function to install packages for macOS
install_macos() {
    echo "Detected macOS. Proceeding with installation."
    # Check if Homebrew is installed
    if ! command -v brew &>/dev/null; then
        echo "Homebrew is not installed. Installing Homebrew."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        echo "Homebrew installed successfully."
    fi

    brew update
    brew upgrade
    brew install \
        cmake \
        eigen \
        gmp \
        mpfr \
        boost \
        gmsh \
        python3 \
        git

    # Ensure command-line tools are installed
    xcode-select --install 2>/dev/null || echo "Command line tools already installed."

    # Install Python testing tool
    pip3 install --upgrade pytest
}

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    install_linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
    install_macos
else
    echo "Unsupported operating system: $OSTYPE"
    exit 1
fi


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
    curl -L -o "$FILENAME" "$URL"

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
        conda activate oncogen
        ;;
    2)
        sed -i '/=/s/=.*//' environment.yml
        sed -i '1s/.*/name: oncogen/' environment.yml
        conda env create -f requirements.yml
        conda activate oncogen
        ;;
    3)
        conda create --name oncogen --file ../OncoGEN/oncogen.txt
        conda activate oncogen
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

pip install --upgrade pip
pip install numpy==1.23.5
pip install nipype==1.7.0 filelock==3.0.0 scikit-image==0.16.2 etelemetry==0.2.0 torch==1.11 nibabel==4.0 dcm2niix tensorboard antspyx==0.4.2

latesttag=$(git describe --tags)
echo "Checking out ${latesttag}"
git checkout ${latesttag}
python setup.py install
echo "BrainMaGe installation successful"
cd ..

echo "Installation of CaPTk"
detect_os
install_captk

if [[ -z "${ONCOGEN_DIR}" ]]; then
    ONCOGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

USER_HOME="$HOME"

add_to_path_unix() {
    if ! grep -q "export ONCOGEN=" ~/.bashrc; then
        echo "export ONCOGEN=$ONCOGEN_DIR" >> ~/.bashrc
        echo "ONCOGEN has been added to your PATH."
        echo "Please run 'source ~/.bashrc' to apply the changes."
    else
        echo "ONCOGEN is already set in your PATH."
    fi
}

add_to_path_macos() {
    if ! grep -q "export ONCOGEN=" ~/.zshrc; then
        echo "export ONCOGEN=$ONCOGEN_DIR" >> ~/.zshrc
        echo 'export PATH="$ONCOGEN/bin:$PATH"' >> ~/.zshrc
        echo "ONCOGEN has been added to your PATH."
        echo "Please run 'source ~/.zshrc' to apply the changes."
    else
        echo "ONCOGEN is already set in your PATH."
    fi
}

add_to_path_windows() {
    local script_file="$HOME/set_config.bat"
    if ! grep -q "setx PATH" "$script_file" 2>/dev/null; then
        echo "@echo off" > "$script_file"
        echo "setx PATH \"%PATH%;$ONCOTUM_DIR\"" >> "$script_file"
        echo "ONCOGEN has been added to your PATH."
        echo "Please restart your command prompt to apply the changes."
    else
        echo "ONCOGEN is already set in your PATH."
    fi
}

create_config_file(){
    CONFIG_FILE="$ONCOTUM_DIR/config.ini"
    {
        echo "[directories]"
        echo "STUDIES_DIR: $USER_HOME/studies/"
        echo "CAPTK_DIR: $USER_HOME/CaPTk/1.8.1/captk"

    } > "$CONFIG_FILE"
    echo "Config file created."
}

case "$(uname -s)" in
    Linux*)     add_to_path_unix ;;
    Darwin*)    add_to_path_macos ;;
    *)          echo "Unsupported OS. Please add the ONCOTUM directory to your PATH manually." ;;
esac

if [[ "$OS" == "Windows_NT" ]]; then
    add_to_path_windows
fi

create_config_file

cd OncoGEN
echo "Installation of prerequisites is completed successfully!"
echo "Some changes require the terminal to be restarted."
echo "Please close and reopen your terminal to apply the changes."
exit 0