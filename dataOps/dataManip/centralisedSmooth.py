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



###  Smooth with a triangular function centered on the mid point
  #  input is the data in list format and a numerical width
  #  smoothing is width range either side of each data point
  #  requires the numpy package





def centralisedSmooth(data=None, width=None):
    import numpy as np

    # construct a list of values increasing from 0 to 1 of size 2*width+1
    # ie: [0.25, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25] for width = 3
    weight = [(_+1)/(width+1) for _ in range(width)] + [1] + [(width-_)/(width+1) for _ in range(width)]
    # create smoothed data list only smoothing by part of weight as approach data limits
    smoothed = [sum(np.multiply(data[:_+width+1],weight[-1*(_+width+1):]))/sum(weight[-1*(_+width+1):]) for _ in range(width)]
    smoothed = smoothed + [sum(np.multiply(data[_-width:_+width+1],weight))/sum(weight) for _ in range(width,len(data)-width,1)]
    smoothed = smoothed + [sum(np.multiply(data[-1*(_+width+1):],weight[:_+width+1]))/sum(weight[:_+width+1]) for _ in range(width)]
    return(smoothed)
