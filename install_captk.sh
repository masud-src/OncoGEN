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

echo "Installation of CaPTk"
cd ..
detect_os
install_captk
cd OncoGEN || exit
