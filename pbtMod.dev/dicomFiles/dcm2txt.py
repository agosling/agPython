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





### simply read in a DICOM file and write it out to a text file

def dcm2txt(file=None):
    from easygui import fileopenbox
    from pydicom.filereader import dcmread

    if file is None:
        file = fileopenbox(msg='msg', title='title', default='*.dcm',
                            filetypes=None, multiple=False)
    elif not file[-3:] is 'dcm':
        file = fileopenbox(msg='msg', title='title', default=file+'*.dcm',
                            filetypes=None, multiple=False)

    dcmText = file[:-3]+'txt'

    with open(dcmText, 'w') as of:
        with dcmread(file) as dcmD:
            of.write(str(dcmD))






###  the following allows the function to run from within this file
  #  will feed the current working directory as a start point to search for
  #  the input file for speed
if __name__ == '__main__':
    from os import getcwd
    dcm2txt(file=getcwd())
