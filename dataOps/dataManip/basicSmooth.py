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



###  a simple centralised 1D data smoothing function
  #  input is the data in list format and a numerical width
  #  smoothing is width range either side of each data point





def basicSmooth(d=None, w=None):

    s = [sum(d[_-w:_+w+1])/(2*w) for _ in range(len(d))]
    return(s)
