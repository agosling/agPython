# agPython

These are a whole range of small sub-functions I have created to help me programming.  
Many of these rely on others within the package.  I have tried to keep it as function based as possible - forking components where I feel it is possible.

*BADGES* - can add badges of metadata such as version info  ([shields.io](https://shields.io/) gives many good options).

## Components

| fileOps | | dataOps | | pbtOps  | |  mcOps  | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `legacy`| fileSplit | `dataClass` | TWODdata | | | | TPStoMC |
| | selectFile | | W2CADdata | | | | |
| | | | pbtDICOM | | | | |
| | | `dataFit` | dosePosition | | | | |
| | | | fitGaussian | | | | |
| | | | fitLine | | | | |
| | | | surface1st/2nd/3rdOrder| | | | |
| | | `dataManip` | basicSmooth| | | | |
| | | | centralisedSmooth| | | | |

###  fileOps

**legacy** -
older files that are now semi-redundant, kept to maintain older

###  dataOps

**dataClass**  -
data classes in for easier data manipulation

**dataManip** -
data manipulation functions, currently for smoothing

**dataFit** -
methods for fitting data

###  pbtOps

### mcOps

# Installation

Clone the repo to a location on your system.

## Requirements

Current laptop `pip freeze`

```
cycler==0.10.0
easygui==0.98.1
kiwisolver==1.0.1
matplotlib==3.0.0
numpy==1.15.2
pandas==0.23.4
pydicom==1.2.2
pyparsing==2.2.1
python-dateutil==2.7.3
pytz==2018.7
scipy==1.1.0
seaborn==0.9.0
six==1.11.0
```

## Tests

Included tests, how to use them, what results to expect

# Usage

Point future python programmes to these files location.  Either add the location of these files to your `$PATH` or use the following commands at the start of each new python programme:

``` python
from sys import path as sysPath
sysPath.append('[PATH TO THESE PACKAGES]'))
```

If you are using multiple file systems, this can be done in a system independent way using the python package `os.path`

Then use:

```python
import agPython
```

# Limitations / Known Bugs

Anything you know doesn't work

# Contribute

Pull requests are welcome.  
For major changes, please open a ticket first to discuss desired changes:  [agPython/issues](http://github.com/agosling/agPython/issues)

If making changes, please check all tests and add if required.

# Licence

All code within this package distributed under [GNU GPL-3.0 (or higher)](https://opensource.org/licenses/GPL-3.0).

Full license text contained within the file LICENCE.

###  (C) License for all programmes

```
###  Copyright (C) 2020:  Andrew J. Gosling

  #  This program is free software: you can redistribute it and/or modify
  #  it under the terms of the GNU General Public License as published by
  #  the Free Software Foundation, either version 3 of the License, or
  #  (at your option) any later version.

  #  This program is distributed in the hope that it will be useful,
  #  but WITHOUT ANY WARRANTY; without even the implied warranty of
  #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  #  GNU General Public License for more details.

  #  You should have received a copy of the GNU General Public License
  #  along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
