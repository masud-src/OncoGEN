import os
import platform
import urllib.request
import zipfile
import subprocess
from setuptools import setup
from setuptools.command.install import install

DCM2NIIX_URLS = {
    'Linux': 'https://github.com/rordenlab/dcm2niix/releases/latest/download/dcm2niix_lnx.zip',
    'Darwin': 'https://github.com/rordenlab/dcm2niix/releases/latest/download/dcm2niix_mac.zip',
    'Windows': 'https://github.com/rordenlab/dcm2niix/releases/latest/download/dcm2niix_win.zip'
}

# Custom Install class to handle downloading and extracting the zip file
class CustomInstallCommand(install):
    def get_sri24(self):
        url = "https://www.nitrc.org/frs/download.php/4841/sri24_spm8.zip//?i_agree=1&download_now=1"

        output_dir = os.path.join(os.path.dirname(__file__), 'data')
        output_file = os.path.join(output_dir, 'sri24.zip')
        unzip_dir = os.path.join(output_dir, 'sri24')

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(unzip_dir, exist_ok=True)

        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, output_file)
        print(f"File downloaded to {output_file}")

        print(f"Unpacking {output_file} to {unzip_dir}...")
        with zipfile.ZipFile(output_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)
        print(f"File unpacked successfully to {unzip_dir}")

        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"Removed zip file: {output_file}")

    def install_dcm2niix(self):
        current_platform = platform.system()

        if current_platform not in DCM2NIIX_URLS:
            raise RuntimeError(f"dcm2niix installation is not supported on {current_platform}.")

        # Download dcm2niix
        url = DCM2NIIX_URLS[current_platform]
        zip_file_path = os.path.join(os.path.dirname(__file__), 'dcm2niix.zip')
        extract_dir = os.path.join(os.path.dirname(__file__))

        # Download the file
        print(f"Downloading dcm2niix from {url}...")
        urllib.request.urlretrieve(url, zip_file_path)
        print(f"Downloaded dcm2niix to {zip_file_path}")

        # Unzip the file
        print(f"Unzipping {zip_file_path}...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Extracted dcm2niix to {extract_dir}")

        # Make sure the binary is executable (for Linux and macOS)
        if current_platform != 'Windows':
            binary_path = os.path.join(extract_dir, 'dcm2niix')
            os.chmod(binary_path, 0o755)
            print(f"Set executable permission for {binary_path}")

        # Remove the zip file
        os.remove(zip_file_path)

    def run(self):
        #install.run(self)
        self.get_sri24()
        self.install_dcm2niix()


# Define the package setup
setup(
    name='OncoGEN',
    version='0.1',
    description='Your package description',
    packages=['OncoGEN'],
    install_requires=[

    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
