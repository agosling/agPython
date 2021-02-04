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





###  fitting a gaussian to spot profile data
  #  need input of the x and y data
  #  init=[amp,mn,sd] are the initial guess values for the gaussian
  #   - (amp)  amplitude of the gaussian
  #   -  (mn)  mean value for the gaussian - centre of the dist
  #   -  (sd)  standard deviation - the width of the gaussian
  #  ideally pass an educated first guess to the function for better fit



def fitGaussian(dataX=None, dataY=None, init=[1,1,1]):
    from numpy import asarray, exp
    from scipy.optimize import curve_fit

    '''  #  will need to check that the data is delivered  '''

    #  ensure that the data is in numpy array format, float type
    dataX = asarray(dataX, dtype=float)
    dataY = asarray(dataY, dtype=float)

    ###  trying to fit with a proper gaussian instead
      #  based on process here:  https://lmfit.github.io/lmfit-py/model.html

    #  defining the gaussian for calculation
    def gaussian(x, amp, mn, sd):
        return amp*exp(-(x-mn)**2/(2*sd**2))

    fit, covar = curve_fit(gaussian, dataX, dataY, p0=init)

    ###  convert the sd of the gaussian to FWHM
      #  FWHM = 2*sqrt(2*ln(2))*sd ~= 2.3548*sd
    fwhm = 2.3548*fit[2]

    #  return is:  fit=[amp,mn,sd], covariance of fit, FWHM
    return(fit, covar, fwhm)
