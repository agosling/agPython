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





###  From Callum
  #  originally named distalDepthSeeker and proximalDepthSeeker

  #  requires the numpy package

  #  input is dose level and x and y data as list formats
  #  Dose level input as % value, i.e.: 80 for 80% dose level



###  finding the position of a dose from the 'start/left' of the distribution
def startingDosePosition(Dose,datax,datay):

    import numpy as np

    '''  #  will need to check that the data is delivered  '''

    #  convert to numpy arrays for simplicity
    datax = np.asarray(datax, dtype=float)
    datay = np.asarray(datay, dtype=float)
    Dose = float(Dose)

    #  check to see if dose alread in %-age
    if np.amax(datay) != 100.0:
        datay = np.divide(datay, np.amax(datay)/100)

    # find first position in file with dose value greater than Dose
    index = np.argmax(datay>Dose)
    if index == len(datay) or index == 0:
        proximal = -1.0
    else:
        y0 = (datay[index-1])
        y1 = (datay[index])
        x0 = (datax[index-1])
        x1 = (datax[index])
        slope = ((y1-y0)/(x1-x0))
        intercept = y0-(slope*x0)
        proximal = (Dose-intercept)/slope
    return proximal;



###  finding the position of a dose from the 'end/right' of the distribution
def endingDosePosition(Dose,datax,datay):

    import numpy as np

    '''  #  will need to check that the data is delivered  '''

    #  convert to numpy arrays for simplicity
    datax = np.asarray(datax, dtype=float)
    datay = np.asarray(datay, dtype=float)
    Dose = float(Dose)

    #  check to see if dose alread in %-age
    if np.amax(datay) != 100.0:
        datay = np.divide(datay, np.amax(datay)/100)

    # find last position in file with dose value greater than Dose
    index = np.argmax(np.flip(datay)>Dose)
    if index == len(datay) or index == 0:
        distal = -1.0
    else:
        y0 = (datay[len(datay)-index-1])
        y1 = (datay[len(datay)-index])
        x0 = (datax[len(datax)-index-1])
        x1 = (datax[len(datax)-index])
        slope = ((y1-y0)/(x1-x0))
        intercept = y0-(slope*x0)
        distal = (Dose-intercept)/slope
    return distal;
