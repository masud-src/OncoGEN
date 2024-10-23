# OncoGEN
Generalisation tool for magnetic resonance images


# Installation

````bash
git clone https://github.com/masud-src/OncoFEM/
````
- First run
````bash
install_brainmage.sh
````
- Download the installer file of CaPTk(https://github.com/CBICA/CaPTk) and run the following commands on Linux:
````bash
chmod +x CaPTk_*_Installer.bin
./CaPTk_*_Installer.bin
````

```python
python3 -m pip install --upgrade setuptools
cd OncoFEM
python3 -m pip install .
```

```python
pip install nibabel ants fslpy
```