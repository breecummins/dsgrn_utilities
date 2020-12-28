# Dependencies

Python 3.7+, DSGRN+dependencies, networkx

# Installation
From the command line, do
```bash
. install.sh
```
or
```text
source install.sh
```
inside of the top-level folder `dsgrn_utilities`. Tests will be run as part of the installation process. One set of tests is dependent on having the `DSGRN` git repository in the same folder as the `dsgrn_utilities` repository, and will fail if that is not true.

# Documentation

Every function has a doc string. The test scripts in the `tests` folder provide some examples on how to use the modules. Limited cases addressed below.

#Commands

This repository is set up as a library, not as a collection of callable scripts. The user is expected to write their own scripts.


## Finding the subset of DSGRN parameters that encompass all monotone Boolean functions


```python
import DSGRN
import dsgrn_utilities.select_boolean_params as sbp

def get_MBFs(networkfile,path2DSGRN):
    network = DSGRN.Network(networkfile)
    MBFs = sbp.subset_boolean_parameters(network,path2DSGRN)
    return MBFs
    
```

The variable `MBFs` is a list of `DSGRN.Parameter` objects. From these, you can work in pure python to find Morse graphs. In some cases, it will be useful to have the parameter indices in order to use a DSGRN database or to find the MBF neighbors. 

To get the parameter indices, do

```python
import DSGRN

def get_MBF_indices(network,MBFs):
    param_graph = DSGRN.ParameterGraph(network)   
    MBF_indices = [param_graph.index(param) for param in MBFs]
    return MBF_indices
    
```

To find the MBF indices and the DSGRN neighbors of the MBFs at the same time, do

```python
import DSGRN
import dsgrn_utilities.get_parameter_neighbors as pn

def get_MBF_neighbors(networkfile, path2DSGRN):
    network = DSGRN.Network(networkfile)
    MBF_indices, neighbors = pn.get_Boolean_parameter_neighbors(network,path2DSGRN)
    return MBF_indices, neighbors
```
The `MBF_indices` do not include duplicates; i.e., those neighbors of MBFs that only exhibit a threshold permutation and therefore are exactly the same MBF. The neighbor list also includes no MBFs, regardless of threshold perturbation. However, the `neighbors` list includes all neighbors of MBFs across all threshold permutations.

# Description of modules
To come.

# Additional Resources

Actively maintained. Contact me via GitHub with any issues or feature requests.


