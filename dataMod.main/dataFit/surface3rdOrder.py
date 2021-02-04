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





###  Find coefficients for surface to fit data
  #  Taken from the site:  https://gist.github.com/amroamroamro/1db8d69b4b65e8bc66a6

  #  data input needs to be in a 2d numpy.array
  #  the exact format must be as created using:  data = np.c_[x, y, z]
  #    where x, y, and z are each lists for every value in the 2D array
  #    ie:   x = [1, 2, 3, 1, 2, 3, 1, 2, 3], y = [1, 1, 1, 2, 2, 2, 3, 3, 3]
  #          z = [1, 2, 3, 2, 4, 6, 3, 6, 9]
  #     -->  data =     x 1 2 3
  #                  y
  #                  1    1 2 3
  #                  2    2 4 6
  #                  3    3 6 9



def surface3rdOrder(data=None):

    import numpy as np
    import scipy.linalg

    '''  #  will need to check that the data is delivered  '''

    mn = np.min(data, axis=0)
    mx = np.max(data, axis=0)

    #  create a grid of values across the range of the data
    #  the 3rd value in each call (not mn[] or mx[]) is how many points
    #  increase this number for "better" fit but slower
    X,Y = np.meshgrid(np.linspace(mn[0], mx[0], 30),
                      np.linspace(mn[1], mx[1], 30))

    #  convert the 2D array to single long list of values
    XX = X.flatten()
    YY = Y.flatten()

    #  best-fit linear plane (1st-order)
    #  start either with an array of 1's, or an array of random numbers
    #  array of random numbers may be better as already has 'shape'
    # A3 = np.c_[np.ones(data.shape[0]),
    #            data[:,:2],
    #            np.prod(data[:,:2], axis=1),
    #            data[:,:2]**2,
    #            np.prod(np.concatenate((data[:,:1]**2, data[:,1:2]), axis=1),
    #                    axis=1),
    #            np.prod(np.concatenate((data[:,:1], data[:,1:2]**2), axis=1),
    #                    axis=1),
    #            data[:,:2]**3]
    A3 = np.c_[np.random.rand(data.shape[0]),
               data[:,:2],
               np.prod(data[:,:2], axis=1),
               data[:,:2]**2,
               np.prod(np.concatenate((data[:,:1]**2, data[:,1:2]), axis=1),
                       axis=1),
               np.prod(np.concatenate((data[:,:1], data[:,1:2]**2), axis=1),
                       axis=1),
               data[:,:2]**3]

    #  use a least square minimisation to find the coefficients of equation
    C3,_,_,_ = scipy.linalg.lstsq(A3, data[:,2])

    # evaluate the solution on a grid
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2,
                     XX**2*YY, XX*YY**2, XX**3, YY**3], C3).reshape(X.shape)

    return(C3,X,Y,Z)
