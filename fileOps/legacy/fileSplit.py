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





###  Split a file path into the directory and filename
  #  for selection starting to use easygui.diropenbox/fileopenbox/filesavebox

  #  https://easygui.readthedocs.io/en/latest/api.html
  #      msg (str) - the message to be displayed
  #      title (str) - the window title

  #  easygui.diropenbox(msg=None, title=None, default=None)
  #      default (str) – starting directory when dialog opens

  #  easygui.fileopenbox(msg=None, title=None, default='*',
  #                      filetypes=None, multiple=False)
  #      default (str) – filepath with wildcards
  #      filetypes (object) – filemasks that a user can choose, e.g. “*.txt”
  #                           list of strings contining filemasks, last string
  #                           is a file type description
  #                           filetypes = ["*.css", ["*.htm", "*.html", "HTML files"] ]
  #      multiple (bool) – If true, more than one file can be selected

  #  easygui.filesavebox(msg=None, title=None, default='', filetypes=None)
  #      default (str) – default filename to return
  #      filetypes (object) – filemasks that a user can choose, e.g. ” *.txt”



def splitFile(file=None):
    from os import path as osPath

    fPath, fName = osPath.split(file)[0], osPath.split(file)[1]

    return(file, fPath, fName)
