from setuptools import setup, find_packages

setup(
    name='oncogen',
    version='0.1.0',
    description='Your package description',
    packages=find_packages(),
    install_requires=[
        'antspyx', 'nibabel', 'fslpy'
    ],
)
