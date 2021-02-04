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



###  using scipy to fit data with a Nth order function
  #  data can have weighting applied to preferentially fit later values in list

  #  returns fit coefficients, fit covariance, and initial guess
  #  fit coeffs correspond to power of x, ie:
  #  coeff[0] for constant, coeff[1] for x, coeff[2] for x**2, etc.





def fitLine(dataX=None, dataY=None, order=None, weights=None):

    from numpy import asarray, flip, polyfit, poly1d

    '''  #  will need to check that the data is delivered  '''

    #  ensure that the data is in numpy array format, float type
    dataX = asarray(dataX, dtype=float)
    dataY = asarray(dataY, dtype=float)

    #  use polyfit to fit to a given order
    if weights == None:
        fit = polyfit(dataX, dataY, order)

    else:
        from numpy import indices
        weights=1/(1+flip(indices(dataX.shape)[0]))
        fit = polyfit(x=dataX, y=dataY, deg=order, w=weights)

    #  creates polynomial using the above coefficients, calculate with
    func = poly1d(fit)

    #  reverse order of coefficients so call by value of power
    #  ie:  fit[2] is coefficient for x**2
    fit = flip(fit)

    return (fit, func)
