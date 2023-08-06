# PyCOGENT

This Python package is for post-processing results from plasma simulation code [COGENT](https://github.com/LLNL/COGENT).

## Installation 

Run the following command to install:

```python
pip install pycogent
```

## Usage

```python
import pycogent as pc

# import data from COGENT 4D-output file with adress 
# "folder/fileName.4d.hdf5", and save it to variable data
data = importData4D("folder/fileName.4d.hdf5")

```

## Help with developing

Tools required to develop pycogent and run tests can be installed with command:

```python
pip install pycogent[dev]
```