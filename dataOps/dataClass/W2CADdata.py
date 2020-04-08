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



###  A W2CAD data class
  #  W2CAD is a Varian data format in a text file
  #  has a very specific structure
  #  Header details what is contained in the file
  #  parameters indicates what each entry contains
  #  for each line, is an x, y, z, and value (often dose)



class W2CADdata:
    def __init__(self):
        self.head = []
        self.params = []
        self.x = []
        self.y = []
        self.z = []
        self.d = []
