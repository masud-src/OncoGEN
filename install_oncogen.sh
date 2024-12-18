#!/bin/bash

echo "Choose the environment: (1) for OncoFEM, (2) for OncoGEN"
read env_choice

if [[ "$env_choice" == "1" ]]; then
  conda init
  conda activate oncofem
elif [[ "$env_choice" == "2" ]]; then
  conda init
  conda activate oncogen
else
  echo "Invalid choice. Please choose either '1' for OncoSTR or '2' for OncoFEM."
  exit 1
fi

if [[ -z "${ONCOGEN_DIR}" ]]; then
    ONCOGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

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
    CONFIG_FILE="$ONCOGEN/config.ini"
    {
        echo "[directories]"
        echo "STUDIES_DIR: $HOME/studies/"
        echo "CAPTK_DIR: $HOME/CaPTk/1.8.1/captk"

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

python -m pip install --upgrade setuptools==60.9.1
python -m pip install .