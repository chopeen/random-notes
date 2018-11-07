# Installation instructions

## 1. Prerequisites

Please make sure you have anaconda installed. Installing by venv/pip is also possible but not recommended.

To do this, check following command:

    conda -V
    > conda 4.5.0
    
Every command run from main directory of the repository.

## 2. First time installation

### Linux/MacOS:

    conda env create -f environment.yml
    source activate types-env


### Windows:

    conda env create -f environment.yml
    activate types-env


## 3. After updates in `environment.yml`, you need to update the environment

    conda env update -f environment.yml
