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





###  generate the spot input values for MC based on the TPS energy
  #  includes potential for multiple TPS models

def TPStoMC(E_TPS=None, model=None):

    if E_TPS == None:
        print('No TPS energy value, exiting...')
        exit()

    if model == None or model == 'SPTC':
        eng = [1.5803, 0.9716]  #  v1
        dsp = [0.1884, 0.0176, -7e-5]  #  v1
        # sxy = [+7.11157e+0, -5.09243e-2, +2.42477e-4, -3.83578e-7]  #  v2 [1e5 histories]
        sxy = [-3.90951501e+02, +2.91159340e+01, -9.17375849e-01,
               +1.62842675e-02, -1.79899435e-04, +1.28504896e-06,
               -5.94603545e-09, +1.72175409e-11, -2.83639671e-14,
               +2.02912243e-17]  #  v3 [5e5 histories]
        # tpi = [+1.71134e+1, -1.87643e-1, +8.83377e-4, -1.51371e-6]  #  v2 [1e5 histories]
        tpi = [+1.40910971e+00, -9.76804265e-02, +2.95503774e-03,
               -5.08280028e-05, +5.47398293e-07, -3.83007653e-09,
               +1.74294759e-11, -4.98095514e-14, +8.12288171e-17,
               -5.76765609e-20]  #  v3 [5e5 histories]
        emt = [+1.43376293e+01, -9.53224309e-01, +2.79171422e-02,
               -4.67503970e-04, +4.92237929e-06, -3.37882649e-08,
               +1.51294106e-10, -4.26541053e-13, +6.87797496e-16,
               -4.83859457e-19]  #  v3 [5e5 histories]

    energy, dispersion, sigmaXY, thetaPhi, emittance = 0,0,0,0,0
    for pwr,cof in enumerate(eng):
        energy += cof*E_TPS**pwr
    for pwr,cof in enumerate(dsp):
        dispersion += cof*E_TPS**pwr
    for pwr,cof in enumerate(sxy):
        sigmaXY += cof*E_TPS**pwr
    for pwr,cof in enumerate(tpi):
        thetaPhi += cof*E_TPS**pwr
    for pwr,cof in enumerate(emt):
        emittance += cof*E_TPS**pwr
    emitt_fac = emittance/(sigmaXY*thetaPhi)
    focus = 'positive'

    # thetaPhi = thetaPhi * 1000  #  to make RAD for the TPS model
    # emittance = emittance * 1000  #  to make RAD for the TPS model

    ###  The following is necessary as the equations aren't quite right
    if emittance/(sigmaXY*thetaPhi) > 3.1:
        emitt_fac = 3.1
        emittance = sigmaXY*thetaPhi*emitt_fac

    GATEinput = {'eng':energy, 'dsp':dispersion, 'sxy':sigmaXY, 'tpi':thetaPhi, 'fac': emitt_fac, 'emt':emittance, 'fcs':focus}

    return(GATEinput)





###  trying to do a something 'better' with modules
  #  based on module development:  https://realpython.com/python-modules-packages/

#  poly1d creates a 1D polynomial from given coefficients
#  input is a list of coefficients starting with highest order value, ie:
#  [2, 3, 4] produces 2x**2 + 3x + 4
from numpy import poly1d

#  creating functions usable within other code
#  ie:  TPStoMC.eng(E_TPS) will return the equivalent value for MC input
eng = poly1d([0.9716, 1.5803])
dsp = poly1d([-7e-5, 0.0176, 0.1884])
# sxy = poly1d([-3.83578e-7, +2.42477e-4, -5.09243e-2, +7.11157e+0])  #  v2 [1e5 histories]
sxy = poly1d([+2.02912243e-17, -2.83639671e-14, +1.72175409e-11,
              -5.94603545e-09, +1.28504896e-06, -1.79899435e-04,
              +1.62842675e-02, -9.17375849e-01, +2.91159340e+01,
              -3.90951501e+02])  #  v3 [5e5 histories]
# tpi = poly1d([-1.51371e-6, +8.83377e-4, -1.87643e-1, +1.71134e+1])  #  v2 [1e5 histories]
tpi = poly1d([-5.76765609e-20, +8.12288171e-17, -4.98095514e-14,
              +1.74294759e-11, -3.83007653e-09, +5.47398293e-07,
              -5.08280028e-05, +2.95503774e-03, -9.76804265e-02,
              +1.40910971e+00])  #  v3 [5e5 histories]
emt = poly1d([-4.83859457e-19, +6.87797496e-16, -4.26541053e-13,
              +1.51294106e-10, -3.37882649e-08, +4.92237929e-06,
              -4.67503970e-04, +2.79171422e-02, -9.53224309e-01,
              +1.43376293e+01])  #  v3 [5e5 histories]
fac = 3.1415
fcs = 'positive'
