"""Package installer."""
import os
from setuptools import setup
from setuptools import find_packages

LONG_DESCRIPTION = ''
if os.path.exists('README.md'):
    with open('README.md') as fp:
        LONG_DESCRIPTION = fp.read()

REQUIREMENTS = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as fp:
        REQUIREMENTS = [
            line.strip()
            for line in fp
        ]

scripts = ['bin/chimaera']

setup(
    name='chimaera',
    version='0.2',
    description='Inferring clonal composition from multiple tumor biopsies',
    long_description=open('README.md').read(),
    author='Matteo Manica',
    author_email='tte@zurich.ibm.com',
    packages=find_packages('.'),
    setup_requires=[
        'Cython'
    ],
    install_requires=[
        'joblib'
        'numpy'
        'scipy'
        'scikit-learn'
        'hdbscan'
        'pandas'
        'xlrd'
    ],
    zip_safe=False,
    scripts=scripts
)
