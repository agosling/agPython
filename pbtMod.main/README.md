Designed based on guide outlined on [makeareadme.com](https://www.makeareadme.com/) but with some personal additions.

---

# TITLE

Brief description of the package/programme etc.

*BADGES* - can add badges of metadata such as version info  ([shields.io](https://shields.io/) gives many good options).

### Components

If formed of multiple parts, outline file structure

## Installation

Steps to take to install

### Requirements

Any specifics, dependencies, use of PipEnv/requirements files

### Tests

Included tests, how to use them, what results to expect

## Usage

Point future python programmes to these files location.  Either add the location
 of these files to your `$PATH` or use the following commands at the start of
 each new python programme (this should be OS independent):

``` python
from sys import path as sysPath
from os import path as osPath
sysPath.append(osPath.join(osPath.expanduser('~'),'[PATH TO THESE PACKAGES]'))
```


## Limitations / Known Bugs

Anything you know doesn't work

## Contribute

Pull requests are welcome.  
For major changes, please open a ticket first to discuss desired changes:  [[repo-name]/issues](http://github.com/agosling/[repo-name]/issues)

If making changes, please check all tests and add if required.

## Licence

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



# pbtMod
General PBT programmes that can run independently or be incorporated into other programmes


## import_dicom_plan.py
script to change certain DICOM headers in plan files so that they will import to Eclipse
