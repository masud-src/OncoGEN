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

python -m pip install --upgrade setuptools
python -m pip install .