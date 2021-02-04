### add python modules folder in OS sensitive fashion
from os import path as osPath
from sys import path as sysPath
sysPath.append(osPath.join(osPath.split(sysPath[0])[0],'packages'))




'''  legacy programmes
# get the FWHM for a singls spot - data should be in a 2D array
def spotProfileFWHM(file=None):
    from fileOps import chooseFile
    import numpy as np
    from dataOps import endingDosePosition, startingDosePosition
    from dataOps import centralisedSmooth

    if file == None:
        file, fpath, fname = chooseFile()
    else:
        fpath, fname = file.rsplit('/', 1)[0], file.rsplit('/', 1)[1]
    chdir(fpath)

    # ['#', ' ', 'n', 'n'] standard data read input for MC output
    # class with .head, .col/rowTitle, and data in .row and .col lists
    data = dataRead(file, ['#', ' ', 'n', 'n'])

    # convert values in data to floats
    data.row = [[float(e) for e in d] for d in data.row]
    data.col = [[float(e) for e in d] for d in data.col]

    # collapse the data in "x" and "y" direction to measure profile
    datax = [sum(d) for d in data.row]
    datay = [sum(d) for d in data.col]

    # create an x data set of 1.0 mm
    x  = [x/10.0 for x in range(1, 1001, 1)]

    x = np.asarray(x, dtype=float)
    datax = np.asarray(datax, dtype=float)
    datax = 100.0*datax/np.max(datax)
    datay = np.asarray(datay, dtype=float)
    datay = 100.0*datay/np.max(datay)

    ###  initial fitting used Callum's code to count up to a dose level
      #  this is very susceptible to noise in the data causing false max
    # smooth the data if desired
    # recommended with minimal width to reduce noise effects
    # COMMENT OUT IF NOT DESIRED
    datax = centralisedSmooth(data=datax, width=2)
    datay = centralisedSmooth(data=datay, width=2)

    # Use Callum's distal and proximal depth dose finders to bootstrap out
    # 50% dose levels either side of Dmax for the spot
    fwhmx = endingDosePosition(50, x, datax) - startingDosePosition(50, x, datax)
    fwhmy = endingDosePosition(50, x, datay) - startingDosePosition(50, x, datay)

    return([fwhmx, fwhmy])






### get the shape for a singls spot
# data should be in a 2D array
# should also supply a list of desired doses - will find on both sides
def spotShape(file=None, doses=[5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95]):
    from fileOps import chooseFile
    import numpy as np
    from dataOps import endingDosePosition, startingDosePosition
    from dataOps import centralisedSmooth
    from os import chdir

    if file == None:
        file, fpath, fname = chooseFile()
    else:
        fpath, fname = file.rsplit('/', 1)[0], file.rsplit('/', 1)[1]
    chdir(fpath)

    # ['#', ' ', 'n', 'n'] standard data read input for MC output
    # class with .head, .col/rowTitle, and data in .row and .col lists
    data = dataRead(file, ['#', ' ', 'n', 'n'])

    # convert values in data to floats
    data.row = [[float(e) for e in d] for d in data.row]
    data.col = [[float(e) for e in d] for d in data.col]

    # collapse the data in "x" and "y" direction to measure profile
    datax = [sum(d) for d in data.row]
    datay = [sum(d) for d in data.col]

    # smooth the data if desired
    # recommended with minimal width to reduce noise effects
    # COMMENT OUT IF NOT DESIRED
    datax = centralisedSmooth(data=datax, width=2)
    datay = centralisedSmooth(data=datay, width=2)

    # create an x data set of 1.0 mm
    x  = [x/10.0 for x in range(1, 1001, 1)]

    x = np.asarray(x, dtype=float)
    datax = np.asarray(datax, dtype=float)
    datax = 100.0*datax/np.max(datax)
    datay = np.asarray(datay, dtype=float)
    datay = 100.0*datay/np.max(datay)

    shapex = []
    shapey = []
    # Use Callum's distal and proximal depth dose finders to bootstrap
    # positions of desired dose levels and Dmax
    for d in doses:
        shapex.append(startingDosePosition(d, x, datax))
        shapey.append(startingDosePosition(d, x, datay))
    shapex.append(startingDosePosition(99.5, x, datax)+0.5*(endingDosePosition(99.5, x, datax) - startingDosePosition(99.5, x, datax)))
    shapey.append(startingDosePosition(99.5, x, datay)+0.5*(endingDosePosition(99.5, x, datay) - startingDosePosition(99.5, x, datay)))
    for d in reversed(doses):
        shapex.append(endingDosePosition(d, x, datax))
        shapey.append(endingDosePosition(d, x, datay))

    fwhmx = endingDosePosition(50, x, datax) - startingDosePosition(50, x, datax)
    fwhmy = endingDosePosition(50, x, datay) - startingDosePosition(50, x, datay)

    return([shapex, shapey], [fwhmx, fwhmy])
'''









from fileOps import chooseDir, dataRead
from os import chdir, listdir
from numpy import asarray
from dataOps import fitGaussian

fpath = chooseDir()
files = [f for f in listdir(fpath) if f.endswith('Dose.txt')]
chdir(fpath)



# fwhm_raw = []  #  no longer needed for newer technique
shape_raw = []
#  legacy from use of endingDosePosition, startingDosePosition
# doses=[5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95]



###  for the code to work in parallel, need to be a contained function
def populateShape(inFile):
    tempShape = []
    # print('fitting gaussian to:  ', inFile)
    var = inFile.split('-')
      #  assume filename format of dosePlane<N>-<E_nominal>-<E_dispersion>-<sigmaXY>-<ThetaPhi>-<Emittance>-<Focus>-Dose.txt
      #  adding the simulation parameters to the output data for a given dataset:
      #    [Energy, Dispersion, SigmaXY, TheataPhi, Emittance, Focus, Plane]
    tempShape.extend([ float(var[1]), float(var[2]), float(var[3]), float(var[4]), float(var[5]), str(var[6]), int(var[0][-1]) ])

    ###  reading in the data to correct format

    #  ['#', ' ', 'n', 'n'] standard data read input for MC output
    #  class with .head, .col/rowTitle, and data in .row and .col lists
    data = dataRead(inFile, ['#', ' ', 'n', 'n'])
    #  convert values in data to floats
    data.row = [[float(e) for e in d] for d in data.row]
    data.col = [[float(e) for e in d] for d in data.col]
    #  collapse the data in "x" and "y" direction to measure profile
    datax = [sum(d) for d in data.row]
    datay = [sum(d) for d in data.col]
    #  create an x data set of 1.0 mm
    x  = [x/10.0 for x in range(1, 1001, 1)]

    #  convert to numpy format
    x = asarray(x, dtype=float)
    datax = asarray(datax, dtype=float)
    datay = asarray(datay, dtype=float)

    ###  performing the gaussian fits
      #  init is the first guess, set for centre of field
      #  return is:  fit=[amp,mn,sd], covariance of fit, FWHM
    fit, _, fwhm = fitGaussian(data_x=x, data_y=datax, init=[1,50,10])
    tempShape.extend([fwhm, fit[1], fit[2]])
    # print('X axis fit results:  ', fwhm, fit)
    fit, _, fwhm = fitGaussian(data_x=x, data_y=datay, init=[1,50,10])
    tempShape.extend([abs(fwhm), fit[1], abs(fit[2])])
    # print('Y axis fit results:  ', fwhm, fit)
    #  legacy from earlier version
    # fitShape, fitFWHM = spotShape(osPath.join(fpath, inFile), doses=doses)
    # tempShape.extend(fitShape[0])
    # tempShape.extend(fitShape[1])
    return(tempShape)


''
###  parallelizing the analysis process for better speed
  #  source:  https://www.machinelearningplus.com/python/parallel-processing-python/
  #  the different uses for pool for different levels of complexity
    #  the simplest is 'map' in which the function is the main argument, and only takes a single iterable for input
  ###  results = pool.map(howmany_within_range_rowonly, [row for row in data])
    #  Next up is 'apply' the function is still the main argument and parameters for the function is the second argumet, apply can then be iterated
  ###  results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
    #  Finally 'starmap' has one iterable argument, but each element in the iterable is also iterable
  ###  results = pool.starmap(howmany_within_range, [(row, 4, 8) for row in data])

  #  using the simplest 'map' option it will run in any order
import multiprocessing as mp

  #  now parallelising the process
pool = mp.Pool(mp.cpu_count())
shape_raw = pool.map(populateShape, [fl for fl in files])
pool.close()
'''
for fl in files:
    shape_raw.append(populateShape(fl))
'''



###  stepping back up to host directory to write output
chdir('..')



### write out the full dataset to a .csv file
# with open('fwhm-data.csv', 'w') as fd:
#     fd.write('Energy,Dispersion,SigmaXY,ThetaPhi,Emittance,Plane,FWHM X,FWHM Y\n')
#     for fwr in fwhm_raw:
#         for _ in fwr:
#             fd.write(str(_) + ',')
#         fd.write('\n')

with open('shape-data.csv', 'w') as sd:
    sd.write(',,,,,,,X,')
    # for _ in doses:
    #     sd.write(',,')
    sd.write(',,,,,,')
    sd.write('Y,\n')
    sd.write('Energy,Dispersion,SigmaXY,ThetaPhi,Emittance,Focus,Plane,')
    # for d in doses:
    #     sd.write(str(d)+'%,')
    # sd.write('Dmax,')
    # for d in reversed(doses):
    #     sd.write(str(d)+'%,')
    # for d in doses:
    #     sd.write(str(d)+'%,')
    # sd.write('Dmax,')
    # for d in reversed(doses):
    #     sd.write(str(d)+'%,')
    sd.write('FWHM X,mean X,stdev X,FWHM Y,mean Y,stdev Y')
    sd.write('\n')
    for shr in shape_raw:
        for _ in shr:
            sd.write(str(_) + ',')
        sd.write('\n')

# plane = list(dict.fromkeys([el[0] for el in fwhm_raw]))
# energy = list(dict.fromkeys([el[1] for el in fwhm_raw]))
# disp = list(dict.fromkeys([el[2] for el in fwhm_raw]))
# sigmaXY = list(dict.fromkeys([el[3] for el in fwhm_raw]))
# thetaphi = list(dict.fromkeys([el[4] for el in fwhm_raw]))
# emit_fac = list(dict.fromkeys([float(round(el[5]/(el[3]*el[4]),2)) for el in fwhm_raw]))
# focus = list(dict.fromkeys([el[6] for el in fwhm_raw]))
#
# print('plane', plane)
# print('energy', energy)
# print('disp', disp)
# print('sigmaXY', sigmaXY)
# print('thetaphi', thetaphi)
# print('emit_fac', emit_fac)
# print('focus', focus)

'''

pln = [1, 2, 3, 4, 5]
# from the first data generation run
# sigmaXY  = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
# thetaPhi = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
# from the second run
# sigmaXY  = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ,0.9, 1.0]
# thetaPhi = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ,0.9, 1.0]
# emit_fac = [0.5, 1.0, 1.5, 1.8, 2.0, 2.3, 2.5, 2.8, 3.0, 3.1]
# from the additional runs
# sigmaXY  = [0.1, 0.3, 0.5, 0.8 ,1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
# thetaPhi = [0.1, 0.3, 0.5, 0.8 ,1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
# emit_fac = [0.1, 0.3, 0.5, 1.0, 1.5, 1.8, 2.0, 2.3, 2.5, 2.8, 3.0, 3.1]

E_TPS = [70, 100, 130, 160, 200, 240]
sigmaXY  = [0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]
thetaPhi = [0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]
emit_fac = [0.1, 1.0, 2.5, 3.1]
focus = 'positive'

###  convert given E_TPS energies into the matching MC energy and dispersion
energy = [((0.0238/0.0222)*(E**1.75))**(1/1.77) for E in E_TPS]
dispersion = [((-1*(0.2562232+(0.0034436*(((0.0238/0.0222)*(E**1.75))**(1/1.77)))))+sqrt((0.2562232+(0.0034436*(((0.0238/0.0222)*(E**1.75))**(1/1.77))))**2-(4*0.4117835*((0.0129581*(((0.0238/0.0222)*(E**1.75))**(1/1.77)))+(0.0000312*(((0.0238/0.0222)*(E**1.75))**(1/1.77))**2)-0.5333012-((0.0487*E)-(0.0000891*E**2)-1.44)))))/(2*0.4117835) for E in E_TPS]



###  fixing extra long floats when generating emit
from decimal import *
getcontext().prec = 3



# calculating the FWHM in X and Y for all variable combinations
fwhm = [[[[[] for _ in range(len(emit_fac))] for _ in range(len(thetaPhi))] for _ in range(len(sigmaXY))] for _ in range(len(pln))]

# also extract the shape of the spot using a range of dose levels
shape = [[[[[] for _ in range(len(emit_fac))] for _ in range(len(thetaPhi))] for _ in range(len(sigmaXY))] for _ in range(len(pln))]
doses=[5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95]

for p,pl in enumerate(pln):
    for s,si in enumerate(sigmaXY):
        for t,tp in enumerate(thetaPhi):
            for e,em in enumerate(emit_fac):
                fwhm[p][s][t][e].extend([pl, si, tp, em])
                shape[p][s][t][e].extend([pl, si, tp, em])
                # fit = spotProfileFWHM(osPath.join(fpath, 'dosePlane' + str(pl) + '-' + str(si) + '-' + str(tp) + '-' + str(si*tp*em) + '-positive-Dose.txt'))
                # fitShape, fitFWHM = spotShape(osPath.join(fpath, 'dosePlane' + str(pl) + '-' + str(si) + '-' + str(tp) + '-' + str(si*tp*em) + '-positive-Dose.txt'), doses=doses)
                ###  fixing extra long floats when generating emit
                fitShape, fitFWHM = spotShape(osPath.join(fpath, 'dosePlane' + str(pl) + '-' + str(si) + '-' + str(tp) + '-' + str(float(Decimal(si)*Decimal(tp)*Decimal(em))) + '-positive-Dose.txt'), doses=doses)
                fwhm[p][s][t][e].extend([fitFWHM[0], fitFWHM[1]])
                shape[p][s][t][e].append(fitShape[0])
                shape[p][s][t][e].append(fitShape[1])

chdir(fpath)
chdir('..')

### write out the full fwhm dataset to a .csv file
with open('fwhm-data.csv', 'w') as fd:
    fd.write('Plane,SigmaXY,ThetaPhi,Emittance,FWHM X,FWHM Y\n')
    for p,pl in enumerate(pln):
        for s,si in enumerate(sigmaXY):
            for t,tp in enumerate(thetaPhi):
                for e,em in enumerate(emit_fac):
                    fd.write(str(pl)+','+str(si)+','+str(tp)+','+str(em)+','+str(fitFWHM[0])+','+str(fitFWHM[1])+'\n')

### write out the full spot shape dataset to a .csv file
with open('shape-data.csv', 'w') as fs:
    fs.write('Plane,SigmaXY,ThetaPhi,Emittance,X,')
    for d in doses:
        fs.write(str(d)+'%,')
    fs.write('Dmax,')
    for d in reversed(doses):
        fs.write(str(d)+'%,')
    fs.write('Y,')
    for d in doses:
        fs.write(str(d)+'%,')
    fs.write('Dmax,')
    for d in reversed(doses):
        fs.write(str(d)+'%,')
    fs.write('\n')
    for p,pl in enumerate(pln):
        for s,si in enumerate(sigmaXY):
            for t,tp in enumerate(thetaPhi):
                for e,em in enumerate(emit_fac):
                    fs.write(str(pl)+','+str(si)+','+str(tp)+','+str(em)+',,')
                    for _ in shape[p][s][t][e]:
                        fs.write(str(_)+',')
                    fs.write('\n')


### write out the data in tabular formats that will allow surface plots
# xy is the list element in the variable fwhm that are the x and y FWHM value
xy = [4,5]
with open('fwhm-tables.csv', 'w') as fo:

    # grouping based on emittance
    for x in xy:
        if x == xy[0]: fo.write('X\n')
        if x == xy[1]: fo.write('Y\n')
        for p,pl in enumerate(pln):
            fo.write('plane,'+str(pl)+'\n')  # title line for each dose plane
            # FWHM separated by the emittance, placing titles
            for em in emit_fac:
                fo.write(',,emittance factor,'+str(em))
                for _ in thetaPhi:
                    fo.write(',')  # spacing for data
            fo.write('\n')
            # titles for each data table
            for _ in emit_fac:
                fo.write(',,thetaphi,')
                for _ in thetaPhi:
                    fo.write(',')  # spacing for data
            fo.write('\n')
            for _ in emit_fac:
                fo.write(',,')
                for tp in thetaPhi:
                    fo.write(str(tp)+',')
                fo.write(',')
            fo.write('\n')
            # write out the lines of data
            for s,si in enumerate(sigmaXY):
                for e,_ in enumerate(emit_fac):
                    fo.write('sigma,'+str(si)+',')
                    for t,_ in enumerate(thetaPhi):
                        fo.write(str(fwhm[p][s][t][e][x])+',')
                    fo.write(',')
                fo.write('\n')
            fo.write('\n\n')
        fo.write('\n\n')

    # grouping based on thetaphi
    for x in xy:
        if x == xy[0]: fo.write('X\n')
        if x == xy[1]: fo.write('Y\n')
        for p,pl in enumerate(pln):
            fo.write('plane,'+str(pl)+'\n')  # title line for each dose plane
            # FWHM separated by the emittance, placing titles
            for tp in thetaPhi:
                fo.write(',,thetaphi,'+str(tp))
                for _ in emit_fac:
                    fo.write(',')  # spacing for data
            fo.write('\n')
            # titles for each data table
            for _ in thetaPhi:
                fo.write(',,emittance,')
                for _ in emit_fac:
                    fo.write(',')  # spacing for data
            fo.write('\n')
            for _ in thetaPhi:
                fo.write(',,')
                for em in emit_fac:
                    fo.write(str(em)+',')
                fo.write(',')
            fo.write('\n')
            # write out the lines of data
            for s,si in enumerate(sigmaXY):
                for t,_ in enumerate(thetaPhi):
                    fo.write('sigma,'+str(si)+',')
                    for e,_ in enumerate(emit_fac):
                        fo.write(str(fwhm[p][s][t][e][x])+',')
                    fo.write(',')
                fo.write('\n')
            fo.write('\n\n')
        fo.write('\n\n')

    # grouping based on sigmaXY  #1 sig  #2 emi
    for x in xy:
        if x == xy[0]: fo.write('X\n')
        if x == xy[1]: fo.write('Y\n')
        for p,pl in enumerate(pln):
            fo.write('plane,'+str(pl)+'\n')  # title line for each dose plane
            # FWHM separated by the emittance, placing titles
            for si in sigmaXY:
                fo.write(',,sigmaXY,'+str(si))
                for _ in thetaPhi:
                    fo.write(',')  # spacing for data
            fo.write('\n')
            # titles for each data table
            for _ in sigmaXY:
                fo.write(',,thetaphi,')
                for _ in thetaPhi:
                    fo.write(',')  # spacing for data
            fo.write('\n')
            for _ in sigmaXY:
                fo.write(',,')
                for tp in thetaPhi:
                    fo.write(str(tp)+',')
                fo.write(',')
            fo.write('\n')
            # write out the lines of data
            for e,em in enumerate(emit_fac):
                for s,_ in enumerate(sigmaXY):
                    fo.write('emittance,'+str(em)+',')
                    for t,tp in enumerate(thetaPhi):
                        fo.write(str(fwhm[p][s][t][e][x])+',')
                    fo.write(',')
                fo.write('\n')
            fo.write('\n\n')
        fo.write('\n\n')


###  grouping based on dose plane - all planes for a given setup on each line
#  want to be able to look at how the spot size changes with distance
# xy is the list element in the variable fwhm that are the x and y FWHM value
#    values 0-3 in fwhm are the plane, sigmaXY, ThetaPhi, and Emittance resp.
xy = [4,5]
with open('fwhm-distance.csv', 'w') as fo:
    fo.write(',,,,,,,X,,,,,Y,,\n')
    fo.write('Energy,Dispersion,SigmaXY,ThetaPhi,Emittance,P1,P2,P3,P4,P5,P1,P2,P3,P4,P5\n')
    for s,si in enumerate(sigmaXY):
        for t,tp in enumerate(thetaPhi):
            for e,em in enumerate(emit_fac):
                fo.write('155,1.3,' + str(si) + ',' + str(tp) + ',' + str(em) + ',')
                for x in xy:
                    for p in range(len(pln)):
                            fo.write(str(fwhm[p][s][t][e][x])+',')
                fo.write('\n')
    fo.write('\n')









###  Going to run through all the files and extract the FWHM
###  Code from runGate.py that generates the files
###   - note:  Emittance is a factor
''
#############################################################################
###  Variables for characterising the spot profiles for a single energy
  #  Use on the beam-character folder in projGATE
sigmaXY  = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
thetaPhi = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
emit_fac = [0.5, 1.0, 1.5, 1.8, 2.0, 2.3, 2.5, 2.8, 3.0, 3.1]
# pre-populate the list of input variables
# callGate = [[] for _ in range(len(sigmaXY)*len(thetaPhi)*len(emit_fac))]
# count = 0
for s in sigmaXY:
    for t in thetaPhi:
        emit = [s*t*_ for _ in emit_fac]
        for e in emit:
            # callGate[count].extend((s,t,e))
            callGate.append('[sigXY,' + str(s) + '] [thetaphi,' + str(t) + '] [emit,' + str(e) + '] [focus,' + str(focus) + ']\' ' + str(fname))
            # count += 1
#############################################################################
'''








'''
# with open('fwhm.csv', 'w') as fo:
#     for p in pln:
#         c = 0
#         fo.write(',,thetaphi\n,plane '+str(p)+',')
#         for t in tpi:
#             fo.write(str(t)+',')
#         fo.write('\nsigma')
#         for s in sig:
#             fo.write(','+str(s))
#             for t in tpi:
#                 fo.write(','+str(fwhm[p-1][c][2]))
#                 # surf[int(p-1),int(s),int(t)] = float(fwhm[p-1][c][2])
#                 c += 1
#             fo.write('\n')
#         fo.write('\n\n')
#
# # print('C[0] + C[1]*x + C[2]*y + C[3]*(x*y) + C[4]*x^2 + C[5]*y^2')
# # print('C[0] + C[1]*Sig + C[2]*ThetaPhi + C[3]*(Sig*ThetaPhi) + C[4]*Sig^2 + C[5]*ThetaPhi^2')
#
# for p in pln:
#     x = [_[0] for _ in fwhm[p-1][:]]
#     y = [_[1] for _ in fwhm[p-1][:]]
#     d = [_[2] for _ in fwhm[p-1][:]]
#     data = np.c_[x, y, d]
#     c = dp.surface2ndOrder(dat = data)
#     print(c)
#
#
# # for 245 MeV test beam setup, planes 1-5 (See macro)
# # x = sigma, y = thetaPhi, z = spot FWHM in mm
# # [0.7997643  2.08615392 0.48116036 0.01941621 0.02994225 0.00989643]
# # [0.95217331 2.07785304 0.69141123 0.01933716 0.02754828 0.00778999]
# # [1.41561534 1.96307034 0.84638512 0.03258073 0.03668011 0.01282332]
# # [2.05096771 1.82846452 0.9869821  0.0456833  0.04604726 0.01624582]
# # [2.72350772 1.71869151 1.0962553  0.06052642 0.05203519 0.01989855]
'''
