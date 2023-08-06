# plico_dm: deformable mirror controller 


 ![Python package](https://github.com/ArcetriAdaptiveOptics/plico_dm/workflows/Python%20package/badge.svg)
 [![codecov](https://codecov.io/gh/ArcetriAdaptiveOptics/plico_dm/branch/main/graph/badge.svg?token=ApWOrs49uw)](https://codecov.io/gh/ArcetriAdaptiveOptics/plico_dm)
 [![Documentation Status](https://readthedocs.org/projects/plico_dm/badge/?version=latest)](https://plico_dm.readthedocs.io/en/latest/?badge=latest)
 [![PyPI version](https://badge.fury.io/py/plico_dm.svg)](https://badge.fury.io/py/plico_dm)


This is part a component of the [plico][plico] framework to control DMs (Alpao, MEMS)


[plico]: https://github.com/ArcetriAdaptiveOptics/plico


## Installation

### Installing

From the wheel

```
pip install plico_dm-XXX.whl
```

In plico_dm source dir

```
pip install .
```

During development you want to update use

```
pip install -e .
```
that install a python egg with symlinks to the source directory in such 
a way that chages in the python code are immediately available without 
the need for re-installing (beware of conf/calib files!)

### Uninstall

```
pip uninstall plico_dm
```

### Config files

The application uses `appdirs` to locate configurations, calibrations 
and log folders: the path varies as it is OS specific. 
The configuration files are copied when the application is first used
from their original location in the python package to the final
destination, where they are supposed to be modified by the user.
The application never touches an installed file (no delete, no overwriting)

To query the system for config file location, in a python shell:

```
import plico_dm
plico_dm.defaultConfigFilePath
```


The user can specify customized conf/calib/log file path for both
servers and client (how? ask!)


## Usage

### Using client 

In a Python / IPython shell:

```
In [1]: import plico_dm

In [2]: dm1=plico_dm.DeformableMirror('AlpaoDM277')

In [3]: dm2=plico_dm.DeformableMirror('MemsMultiDM')

In [4]: dm1.getSnapshot('boo')
Out[4]: {'boo.COMMAND_COUNTER': 0, 'boo.SERIAL_NUMBER': '1', 'boo.STEP_COUNTER': 45956}

In [5]: dm1.applyZonalCommand(np.ones(277))

In [6]: dm1.getZonalCommand()
Out[6]:
array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1.])

In [7]: dm1.getSnapshot('boo')
Out[7]: {'boo.COMMAND_COUNTER': 1, 'boo.SERIAL_NUMBER': '1', 'boo.STEP_COUNTER': 83589}

In [8]: dm2.getSnapshot('tux')
Out[8]:
{'tux.COMMAND_COUNTER': 0,
 'tux.SERIAL_NUMBER': '234',
 'tux.STEP_COUNTER': 95980}
```

