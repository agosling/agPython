#  Packages

These packages have been developed to help me in coding.

| fileOps | | dataOps | | pbtOps  | |  mcOps  | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | `dataClass`  | TWODdata  | | | | |
| | |              | W2CADdata | | | | |
| | | `dicomClass` | | | | | |
| | | `dataSmooth` | | | | | |
| | | `dataFit`    | | | | | |


# Usage

After cloning to your computer, you must point future python programmes to these files.  Either add the location of these files to your `$PATH` or use the following commands at the start of each new python programme:

``` python
from sys import path as sysPath
sysPath.append('[PATH TO THESE PACKAGES]'))
```

If you are using multiple file systems, this can be done in a system independent way using the python package `os.path`

Then use:

```python
import agPython
```

#  Contents

###  fileOps

###  dataOps

#####  dataClass
data classes in for easier data manipulation

#####  dicomClass
subset of full DICOM data class for easier handling

#####  dataSmooth
data smoothing functions

#####  dataFit
methods for fitting data

###  pbtOps

###  mcOps


#  Known Issues

# Licence

All code within this package distributed under [GNU GPL-3.0 (or higher)](https://opensource.org/licenses/GPL-3.0).

Full license text contained within the file LICENCE.

The below text should be included at the start of each file.

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
