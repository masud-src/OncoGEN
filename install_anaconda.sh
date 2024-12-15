#!/bin/bash

OS=$(uname -s)
ARCH=$(uname -m)

if [[ "$OS" == "Linux" ]]; then
    OS="Linux"
elif [[ "$OS" == "Darwin" ]]; then
    OS="MacOSX"
elif [[ "$OS" =~ MINGW64 || "$OS" =~ MSYS ]]; then
    OS="Windows"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

if [[ "$OS" == "MacOSX" && "$ARCH" == "arm64" ]]; then
    ARCH="arm64"
elif [[ "$ARCH" == "x86_64" ]]; then
    ARCH="x86_64"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

cd ..
URL="https://repo.anaconda.com/archive/Anaconda3-latest-$OS-$ARCH.sh"
echo "Downloading Anaconda installer from: $URL"
curl -o AnacondaInstaller.sh "$URL"
bash Anaconda.sh -b -p $HOME/anaconda3
eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
conda init
cd OncoGEN
echo "Installation of anaconda is completed successfully!"
echo "Some changes require the terminal to be restarted."
echo "Please close and reopen your terminal to apply the changes."
exit 0