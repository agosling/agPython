### add python modules folder in OS sensitive fashion
from os import path as osPath
from sys import path as sysPath
sysPath.append(osPath.join(osPath.split(sysPath[0])[0],'packages'))



### [ene,69.39452] [disp,1.08082] [sigXY,11.91123???] [thetaphi,8.507836522239193] [emit,308.43594] [focus,positive]

def tpsToMCinput(E_TPS=None, emit=None):
    from math import sqrt
      #  may need to re-visit to get polynomial solution for MC input reasons.
    energy = ((0.0238/0.0222)*(E_TPS**1.75))**(1/1.77)
    dispersion = ((-1*(0.2562232+(0.0034436*(((0.0238/0.0222)*(E_TPS**1.75))**(1/1.77)))))+sqrt((0.2562232+(0.0034436*(((0.0238/0.0222)*(E_TPS**1.75))**(1/1.77))))**2-(4*0.4117835*((0.0129581*(((0.0238/0.0222)*(E_TPS**1.75))**(1/1.77)))+(0.0000312*(((0.0238/0.0222)*(E_TPS**1.75))**(1/1.77))**2)-0.5333012-((0.0487*E_TPS)-(0.0000891*E_TPS**2)-1.44)))))/(2*0.4117835)
    sigmaXY = 7.94235454 - 5.89765501e-02*E_TPS + 2.67045266e-04*E_TPS**2 - 4.05447861e-07*E_TPS**3
    thetaPhi = 1.88808896e+01 - 1.72114043e-01*E_TPS + 8.05647969e-04*E_TPS**2 - 1.31175534e-06*E_TPS**3
    #  seems like need close to maximum emit at least to start - will then need to adjust
    emitt_fac = 3.1415
    emittance = sigmaXY * thetaPhi * emitt_fac  #  emit
    focus = 'positive'
    # focus = 'negative'
    sigmaXY = 3.585
    thetaPhi = 3.6586
    # emittance = 135.90708
    GATEinput = {'ene':energy, 'disp':dispersion, 'sigXY':sigmaXY, 'thetaphi':thetaPhi, 'efac': emitt_fac, 'emit':emittance, 'focus':focus}
    return(GATEinput)





#############################################################################
#############################################################################
#############################################################################





###  run the MC for a given set of input
  #  return the location and names of the output files
def runMC(log, input=None):
    ###  generate a beam and deliver in air
    ###  measure profile at 100 mm intervals either side of origin
      #  FOR FUTURE:  allow to pass position of planes for measure


      #  generate the monte carlo input command
    callGATE = 'gate -a \'[n,1] '
    for key in input.keys():
        if isinstance(input[key], float) and key is not 'efac':
            callGATE+='['+key+','+str(round(input[key],5))+'] '
    callGATE+='[focus,'+str(input['focus'])+']\' '+str(input['fileName'])
    callGATE+=' > output/gate-log-'+str(input['ene']).split('.')[0]+'.txt' # &'
      #  don't include the '&' if want to make it work with subprocess
      #  the '&' puts process in background so .wait() doesn't register

      #  run the command as a subprocess
      #  use .wait() to not continue until complete
    from subprocess import Popen as subprocessPopen
    from os import getcwd, chdir
    currDir = getcwd()
    chdir(input['filePath'])
    log.write('subprocessPopen:  \n' + str(callGATE) + '\n')
    subprocessPopen(callGATE, shell=True).wait()
    log.write('   MC completed\n' + '\n')
    chdir(currDir)

    return()





#############################################################################
#############################################################################
#############################################################################





###  a subprogramme to read in some data then fit a gaussian in X and Y
def measureMCgaussian(file=None):
    ###  read in and get the data into correct format
    from fileOps import dataRead
      #  ['#', ' ', 'n', 'n'] standard data read input for MC output
      #  class with .head, .col/rowTitle, and data in .row and .col lists
    data = dataRead(file, ['#', ' ', 'n', 'n'])
      #  convert values in data to floats
    data.row = [[float(e) for e in d] for d in data.row]
    data.col = [[float(e) for e in d] for d in data.col]
      #  collapse the data in "x" and "y" direction to measure profile
    datax = [sum(d) for d in data.row]
    datay = [sum(d) for d in data.col]
      #  create an x data set of 1.0 mm
    x  = [x/10.0 for x in range(1, 1001, 1)]
      #  convert to numpy format
    from numpy import asarray
    x = asarray(x, dtype=float)
    datax = asarray(datax, dtype=float)
    datay = asarray(datay, dtype=float)

    ###  smoothing if desired - may help speed up by needing less histories
    from dataOps import centralisedSmooth
    datax = centralisedSmooth(data=datax, width=3)
    datay = centralisedSmooth(data=datay, width=3)

    ###  fit a guassian to the data for both axes
    from dataOps import fitGaussian
      #  init is the first guess, set for centre of field
      #  return is:  fit=[amp,mn,sd], covariance of fit, FWHM
    fitx, _, fwhmx = fitGaussian(dataX=x, dataY=datax, init=[1,50,10])
    fity, _, fwhmy = fitGaussian(dataX=x, dataY=datay, init=[1,50,10])

    return([abs(fwhmx), abs(fitx[1]), abs(fitx[2]), abs(fwhmy), abs(fity[1]), abs(fity[2])])





#############################################################################
#############################################################################
#############################################################################





def measureFWHM(log, input=None):
    ###  measure the FWHM of the spot profile
    ###  return the measured FWHM
      #  FOR FUTURE:  allow to pass position of planes for measure
      #  input should be a dictionary of MC input values

    log.write('measuring the FWHM at each plane' + '\n')
    from os import path as osPath, remove
    gFit = []
    for pln in range(5):
        outFile = osPath.join(input['filePath'],'output','dosePlane'+str(pln+1))
        for key in input.keys():
            if isinstance(input[key], float) and key is not 'efac':
                outFile+='-'+str(round(input[key],5))
        outFile+='-'+str(input['focus'])+'-Dose.txt'
        # log.write(' measuring in:  ' + str(outFile) + '\n')
        gFit.append(measureMCgaussian(outFile))
      #  remove the output files to stop filling up the drive with data files
        # log.write('removing file:  ' + str(outFile) + '\n')
        remove(outFile)
        remove(outFile.rsplit('-',1)[0]+'-Dose-Squared.txt')
        remove(outFile.rsplit('-',1)[0]+'-Dose-Uncertainty.txt')
    log.write('   removed the output files to save space\n' + '\n')

    return(gFit)





#############################################################################
#############################################################################
#############################################################################





def simFitFWHM(log, Ginput=None, pos=None):
      #  2D array, an entry for each plane, data contained is:
      #  currFit_XXX = [fwhmX, meanX, stdevX, fwhmY, meanY, stdevY]
    from dataOps import fitLine

    runMC(log, input=Ginput)
    currFit = measureFWHM(log, input=Ginput)
    fit, eqn = fitLine(pos, [_[0] for _ in currFit], 2)  #  X FWHM for each plane from MC

    # fwhm_record, sigma_record, theta_record, emitt_record
    record = [[_[0] for _ in currFit],\
              [Ginput['sigXY'], fit[0]],\
              [Ginput['thetaphi'], fit[1]],\
              [Ginput['emit'], Ginput['emit']/(Ginput['sigXY']*Ginput['thetaphi']), fit[2]]]
    '''  For sigXY may want to return the eqn rather than fit[0]
        spot size more position dependent so may want to fit at nozzle or iso  '''

    return(fit, eqn, record)





#############################################################################
#############################################################################
#############################################################################





def iterativeProfileFit(Etps):

    ##  read in a template GATE macro to base calculations on
    from os import path as osPath, getcwd, chdir
    file = osPath.join(getcwd(),'MC-profile','characterize-beam-profile.mac')
    fPath, fName = osPath.split(file)[0], osPath.split(file)[1]
    # chdir(fPath)

    ###  will be doing a lot of line fitting as part of this
    from dataOps import fitLine, weightedFitLine



    ###  The TPS data to be fit
    plane1 = [12.247, 11.706, 11.293, 11.019, 10.807, 10.641, 10.548, 10.364, 10.162, 9.98, 9.813, 9.645, 9.547, 9.312, 9.249, 9.114, 9.066, 9.037, 9.107, 9.241, 9.254, 9.23, 9.2, 9.001, 8.922, 8.799, 8.77, 8.73, 8.714, 8.795, 8.89, 8.978, 8.931, 8.838, 8.754, 8.66]
    plane2 = [13.246, 12.613, 12.126, 11.796, 11.485, 11.291, 11.14, 10.923, 10.74, 10.507, 10.311, 10.132, 9.941, 9.753, 9.703, 9.509, 9.381, 9.349, 9.392, 9.478, 9.482, 9.434, 9.33, 9.222, 9.082, 8.973, 8.919, 8.881, 8.89, 8.9, 9.015, 9.009, 9.024, 8.941, 8.825, 8.786]
    plane3 = [14.394, 13.691, 13.174, 12.708, 12.337, 12.048, 11.824, 11.575, 11.312, 11.058, 10.786, 10.594, 10.404, 10.218, 10.133, 9.938, 9.8, 9.714, 9.718, 9.735, 9.74, 9.681, 9.609, 9.461, 9.3, 9.176, 9.135, 9.085, 9.089, 9.096, 9.16, 9.172, 9.155, 9.085, 8.945, 8.871]
    plane4 = [15.697, 14.882, 14.252, 13.786, 13.292, 12.971, 12.613, 12.324, 12.06, 11.761, 11.485, 11.271, 10.994, 10.853, 10.752, 10.495, 10.32, 10.222, 10.201, 10.142, 10.121, 10.002, 9.877, 9.804, 9.6, 9.495, 9.415, 9.369, 9.363, 9.338, 9.383, 9.415, 9.369, 9.281, 9.136, 9.072]
    plane5 = [16.908, 16.094, 15.299, 14.728, 14.241, 13.808, 13.404, 13.054, 12.747, 12.41, 12.108, 11.83, 11.573, 11.404, 11.22, 11.03, 10.788, 10.682, 10.59, 10.531, 10.477, 10.387, 10.223, 10.094, 9.945, 9.788, 9.715, 9.654, 9.615, 9.576, 9.609, 9.562, 9.566, 9.476, 9.313, 9.238]

    TPS_energies = [70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 244]

    TPS_profiles={}
    for et,tpse in enumerate(TPS_energies):
        TPS_profiles[tpse] = [plane1[et], plane2[et], plane3[et], plane4[et], plane5[et]]



    ###  measure the reference values to match
      #  combine the TPS FWHM fit data
      #  consider closest plane to be -ve value
    TPSposition = [-191.0, -100.0, 0.0, 100.0, 189.0]
    position = [-200.0, -100.0, 0.0, 100.0, 200.0]
    # TPSfwhm = [plane1[et], plane2[et], plane3[et], plane4[et], plane5[et]]
      #  returns coefficients in order of power, ie: C[2] = C*X**2
      #  Nth order fit to the TPS FWHM fit
      #  2nd order fit definitely best reflects shape
    # TPSfit, TPSeqn = fitLine(TPSposition, TPSfwhm, 2)
    TPSfit, TPSeqn = fitLine(TPSposition, TPS_profiles[Etps], 2)



    ###  generate the associated MC input values for a given TPS energy
      #  initial guesses using the analytical fits
    GATEinput = tpsToMCinput(E_TPS=Etps)
    GATEinput['filePath'] = fPath
    GATEinput['fileName'] = fName
      #  open a file to write a log of the fitting
    log = open(osPath.join(fPath,'output','matching-log-'+str(GATEinput['ene']).split('.')[0]+'MeV.txt'), 'w')






    ###  Need "previous guesses" to get the fitting started
    GATEinput['sigXY'] = 0.95*GATEinput['sigXY']
    GATEinput['thetaphi'] = 0.95*GATEinput['thetaphi']
    GATEinput['efac'] = 0.95 * 3.1415
    GATEinput['emit'] = GATEinput['sigXY'] * GATEinput['thetaphi'] * GATEinput['efac']

    # MCXfit, MCXeqn, MCrecord = simFitFWHM(log, Ginput=GATEinput, pos=position)
    # the above equates to this:
    runMC(log, input=GATEinput)
    currFit = measureFWHM(log, input=GATEinput)
    MCXfit, MCXeqn = fitLine(position, [_[0] for _ in currFit], 2)  #  X FWHM for each plane from MC
    fwhm_record = [[_[0] for _ in currFit]]   # [FWHM @ each plane]
    sigma_record = [[GATEinput['sigXY'], MCXfit[0]]]  # [sigXY, spot size @ iso]
    theta_record = [[GATEinput['thetaphi'], MCXfit[1]]]  # [thetaphi, slope of fit]
    emitt_record = [[GATEinput['efac'], GATEinput['emit'], MCXfit[2]]]  # [emitt_fac, emittance, curve of fit]
    # full_record = [[fwhm_record[-1], sigma_record[-1], theta_record[-1], emitt_record[-1]]]


    ###  Regenerate the associated MC data for a given input set
      #  initial guesses using the analytical fits
    GATEinput['sigXY'] = GATEinput['sigXY']/0.95
    GATEinput['thetaphi'] = GATEinput['thetaphi']/0.95
    GATEinput['efac'] = 3.1415
    GATEinput['emit'] = GATEinput['sigXY'] * GATEinput['thetaphi'] * GATEinput['efac']



    ###  now iterate over the input values until have a good match
    # while (abs(MCXfwhm[_]-TPSfwhm[_]) > 0.1 for _ in range(5)):
    while True:

        import matplotlib.pyplot as plt

        ###  Estimate a better fit for thetaphi, based on slope of FWHM vals
        while True:
              #  run and measure the FWHM data for the new input values
            # MCXfit, MCXeqn, MCrecord = simFitFWHM(log, Ginput=GATEinput, pos=position)
            # full_record.append(MCrecord)
            # fwhm_record.append(MCrecord[0])  # [FWHM @ each plane]
            # # sigma_record.append(MCrecord[1])  # [sigXY, spot size @ iso]
            # theta_record.append(MCrecord[2])  # [thetaphi, slope of fit]
            # # emitt_record.append(MCrecord[3])  # [emittance, emit_fac, curve of fit]
              #  the above equates to this:
            runMC(log, input=GATEinput)
            currFit = measureFWHM(log, input=GATEinput)
            MCXfit, MCXeqn = fitLine(position, [_[0] for _ in currFit], 2)  #  X FWHM for each plane from MC
            fwhm_record.append([_[0] for _ in currFit])   # [FWHM @ each plane]
            # sigma_record.append([GATEinput['sigXY'], MCXfit[0]])  # [sigXY, spot size @ iso]
            theta_record.append([GATEinput['thetaphi'], MCXfit[1]])  # [thetaphi, slope of fit]
            # emitt_record.append([GATEinput['efac'], GATEinput['emit'], MCXfit[2]])  # [emit_fac, emittance, curve of fit]
            # full_record.append([fwhm_record[-1], sigma_record[-1], theta_record[-1], emitt_record[-1]])

            # log.write(' full_record:  \n' + str(full_record) + '\n' + '\n')
            log.write('theta_record:  \n' + str(theta_record) + '\n')
            log.write('\n   TPSfit:  '+ str(TPSfit[1]) + '\n')
            log.write('   MCXfit:  ' + str(MCXfit[1]) + '\n')
            log.write('frac diff:  ' + str((MCXfit[1]-TPSfit[1])/TPSfit[1]) + '\n')
            log.write('\n' + '\n')
            log.write(str(TPS_profiles[Etps]) + '\n')
            log.write(str([round(_,3) for _ in fwhm_record[-1]]) + '\n')
            log.write(str([round(fwhm_record[-1][_]-TPS_profiles[Etps][_],3) for _ in range(5)]) + '\n')
            log.write('\n\n')

              #  check to see if slope now matches TPS
            if abs((MCXfit[1]-TPSfit[1])/TPSfit[1]) < 0.05:
                log.write('\n\n\n' + '\n')
                log.write('  #  ThetaPhi matched' + '\n')
                log.write('ThetaPhi:  ' + str(GATEinput['thetaphi']) + '\n')
                log.write('\n\n\n' + '\n')
                break

              #  if doesn't fit then fit relationship for a new thetaphi
            spotSlopeFit, FITeqn = fitLine([_[0] for _ in theta_record], [_[1] for _ in theta_record], 1)
              #  Trial using an inverse weighting to fit the line
              #  prioritises more recent estimates - quicker convergence???
            # spotSlopeFit, FITeqn = weightedFitLine([_[0] for _ in theta_record], [_[1] for _ in theta_record], 1, 1)

              #  have to record previous emittance factor
            GATEinput['thetaphi'] = (TPSfit[1]-spotSlopeFit[0])/spotSlopeFit[1]
            if GATEinput['thetaphi'] < 0.00001:  GATEinput['thetaphi'] = 0.00001
              #  also have to update emittance
            GATEinput['emit'] = GATEinput['sigXY']*GATEinput['thetaphi']*GATEinput['efac']

            log.write('\nnew GATEinput[\'thetaphi\'] - ' + str(GATEinput['thetaphi']) + '\n')
            log.write('\n\n\n' + '\n')

            # plt.close('all')  # need 'all' otherwise interferes with .wait() elsewhere
            plt.close('tpi')
            plt.figure(num='tpi')
            plt.scatter([_[0] for _ in theta_record], [_[1] for _ in theta_record], c=list(range(len(theta_record))), cmap='Wistia')
            plt.title('thetaPhi:  ' + str(Etps))
            plt.plot([_[0] for _ in theta_record], FITeqn([_[0] for _ in theta_record]), '-')
            plt.plot([_[0] for _ in theta_record], [TPSfit[1] for _ in theta_record], '-')
            plt.plot(GATEinput['thetaphi'], 0, 'o')
            plt.show(block=False)
            plt.pause(0.10)  # wait before next action for plt

            plt.close('fwhm')
            plt.figure(num='fwhm')
            plt.title('fwhm:  ' + str(Etps))
            plt.plot(TPSposition, TPS_profiles[Etps], 'o')
            plt.plot(position, fwhm_record[-1], '-')
            # plt.pause(10)  # wait before next action for plt
            plt.show(block=False)
            plt.pause(0.10)  # wait before next action for plt


        ###  Estimate a better fit for sigXY, based on FWHM at isocentre
          #  factor of 0.5 as FWHM is "diameter", sigXY is radius
        while True:
              #  run and measure the FWHM data for the new input values
            # MCXfit, MCXeqn, MCrecord = simFitFWHM(log, GATEinput=GATEinput, pos=position)
            # full_record.append(MCrecord)
            # fwhm_record.append(MCrecord[0])  # [FWHM @ each plane]
            # sigma_record.append(MCrecord[1])  # [sigXY, spot size @ iso]
            # # theta_record.append(MCrecord[2])  # [thetaphi, slope of fit]
            # # emitt_record.append(MCrecord[3])  # [emittance, emit_fac, curve of fit]
              #  the above equates to this:
            runMC(log, input=GATEinput)
            currFit = measureFWHM(log, input=GATEinput)
            MCXfit, MCXeqn = fitLine(position, [_[0] for _ in currFit], 2)  #  X FWHM for each plane from MC
            fwhm_record.append([_[0] for _ in currFit])   # [FWHM @ each plane]
            sigma_record.append([GATEinput['sigXY'], MCXfit[0]])  # [sigXY, spot size @ iso]
            # theta_record.append([GATEinput['thetaphi'], MCXfit[1]])  # [thetaphi, slope of fit]
            # emitt_record.append([GATEinput['efac'], GATEinput['emit'], MCXfit[2]])  # [emit_fac, emittance, curve of fit]
            # full_record.append([fwhm_record[-1], sigma_record[-1], theta_record[-1], emitt_record[-1]])
            # log.write(' full_record:  \n' + str(full_record) + '\n' + '\n')
            log.write('sigma_record:  \n' + str(sigma_record) + '\n')
            log.write('\n   TPSfit:  ' + str(TPSfit[0]) + '\n')
            log.write('   MCXfit:  ' + str(MCXfit[0]) + '\n')
            log.write('frac diff:  ' + str((MCXfit[0]-TPSfit[0])/TPSfit[0]) + '\n')
            log.write('\n' + '\n')
            log.write(str(TPS_profiles[Etps]) + '\n')
            log.write(str([round(_,3) for _ in fwhm_record[-1]]) + '\n')
            log.write(str([round(fwhm_record[-1][_]-TPS_profiles[Etps][_],3) for _ in range(5)]) + '\n')
            log.write('\n')

              #  check to see if central spot FWHM matches TPS
            if abs(MCXfit[0]-TPSfit[0]) < 0.1:
                log.write('\n\n\n' + '\n')
                log.write('  #  SigmaXY matched' + '\n')
                log.write('SigmaXY:  ' + str(GATEinput['sigXY']) + '\n')
                log.write('\n\n\n' + '\n')
                break

              #  if doesn't fit then estimate a new sigXY
            spotSizeFit, FITeqn = fitLine([_[0] for _ in sigma_record], [_[1] for _ in sigma_record], 1)
              #  Trial using an inverse weighting to fit the line
              #  prioritises more recent estimates - quicker convergence???
            # spotSizeFit, FITeqn = weightedFitLine([_[0] for _ in sigma_record], [_[1] for _ in sigma_record], 1, 1)
            GATEinput['sigXY'] = (TPSfit[0]-spotSizeFit[0])/spotSizeFit[1]
            if GATEinput['sigXY'] < 0.00001:  GATEinput['sigXY'] = 0.00001
              #  also have to update emittance
            GATEinput['emit'] = GATEinput['sigXY']*GATEinput['thetaphi']*GATEinput['efac']

            log.write('\nnew GATEinput[\'sigXY\'] - ' + str(GATEinput['sigXY']) + '\n')
            log.write('\n\n\n' + '\n')

            # plt.close('all')  # need 'all' otherwise interferes with .wait() elsewhere
            plt.close('sig')
            plt.figure(num='sig')
            plt.scatter([_[0] for _ in sigma_record], [_[1] for _ in sigma_record], c=list(range(len(sigma_record))), cmap='Wistia')
            plt.title('SigmaXY:  ' + str(Etps))
            plt.plot([_[0] for _ in sigma_record], FITeqn([_[0] for _ in sigma_record]), '-')
            plt.plot([_[0] for _ in sigma_record], [TPSfit[0] for _ in sigma_record], '-')
            plt.plot(GATEinput['sigXY'], 0, 'o')
            plt.show(block=False)
            plt.pause(0.10)  # wait before next action for plt

            plt.close('fwhm')
            plt.figure(num='fwhm')
            plt.title('fwhm:  ' + str(Etps))
            plt.plot(TPSposition, TPS_profiles[Etps], 'o')
            plt.plot(position, fwhm_record[-1], '-')
            # plt.pause(10)  # wait before next action for plt
            plt.show(block=False)
            plt.pause(0.10)  # wait before next action for plt


        '''   ###  Wonder if use efac instead of emit when matching???
        ###  Estimate a better fit for emittance based on 2nd order of fits
        while True:
              #  run and measure the FWHM data for the new input values
            # MCXfit, MCXeqn, MCrecord = simFitFWHM(log, Ginput=GATEinput, pos=position)
            # full_record.append(MCrecord)
            # fwhm_record.append(MCrecord[0])  # [FWHM @ each plane]
            # # sigma_record.append(MCrecord[1])  # [sigXY, spot size @ iso]
            # # theta_record.append(MCrecord[2])  # [thetaphi, slope of fit]
            # emitt_record.append(MCrecord[3])  # [emittance, emit_fac, curve of fit]
              #  the above equates to this:
            runMC(log, input=GATEinput)
            currFit = measureFWHM(log, input=GATEinput)
            MCXfit, MCXeqn = fitLine(position, [_[0] for _ in currFit], 2)  #  X FWHM for each plane from MC
            fwhm_record.append([_[0] for _ in currFit])   # [FWHM @ each plane]
            # sigma_record.append([GATEinput['sigXY'], MCXfit[0]])  # [sigXY, spot size @ iso]
            # theta_record.append([GATEinput['thetaphi'], MCXfit[1]])  # [thetaphi, slope of fit]
            emitt_record.append([GATEinput['emit'], GATEinput['emit']/(GATEinput['sigXY']*GATEinput['thetaphi']), MCXfit[2]])  # [emittance, emit_fac, curve of fit]
            # full_record.append([fwhm_record[-1], sigma_record[-1], theta_record[-1], emitt_record[-1]])
            # log.write(' full_record:  \n' + str(full_record) + '\n' + '\n')
            log.write('emitt_record:  \n' + str(emitt_record) + '\n')
            log.write('\n   TPSfit:  ' + str(TPSfit[2]) + '\n')
            log.write('   MCXfit:  ' + str(MCXfit[2]) + '\n')
            log.write('frac diff:  ' + str((MCXfit[2]-TPSfit[2])/TPSfit[2]) + '\n')
            log.write('\n' + '\n')
            log.write(str(TPS_profiles[Etps]) + '\n')
            log.write(str([round(_,3) for _ in fwhm_record[-1]]) + '\n')
            log.write(str([round(fwhm_record[-1][_]-TPS_profiles[Etps][_],3) for _ in range(5)]) + '\n')
            log.write('\n')

              #  check to see if curve now matches TPS
            if abs((MCXfit[2]-TPSfit[2])/TPSfit[2]) < 0.05:
                log.write('\n\n\n' + '\n')
                log.write('  #  Emittance matched' + '\n')
                log.write('Emittance:  ' + str(GATEinput['emit']) + '\n')
                log.write('\n\n\n' + '\n')
                break
            elif len(emitt_record) > 4 and all(emitt_record[_][0] == emitt_record[-1][0] for _ in range(-4,-1)):
                log.write('\n\n\n' + '\n')
                log.write('  #  Emittance stuck!' + '\n')
                log.write('Emittance:  ' + str(GATEinput['emit']) + '\n')
                log.write(' factor:    ' + str(emitt_record[-1][1]) + '\n')
                ''
                log.write('Perhaps changing the focus will help??????')
                log.write('   Focus was ' + str(GATEinput['focus'])
                if GATEinput['focus'] == 'positive':  GATEinput['focus'] = 'negative'
                elif GATEinput['focus'] == 'negative':  GATEinput['focus'] = 'positive'
                log.write('   Focus is now ' + str(GATEinput['focus'])
                log.write('\n\n\n')
                ''
                break


              #  if doesn't fit then estimate a new emittance factor
            spotCurveFit, FITeqn = fitLine([_[0] for _ in emitt_record], [_[2] for _ in emitt_record], 1)
              #  Trial using an inverse weighting to fit the line
              #  prioritises more recent estimates - quicker convergence???
            # spotCurveFit, FITeqn = weightedFitLine([_[0] for _ in emitt_record], [_[2] for _ in emitt_record], 1, 1)
            GATEinput['emit'] = (TPSfit[2] - spotCurveFit[0])/spotCurveFit[1]
            emit_fac = GATEinput['emit']/(GATEinput['sigXY']*GATEinput['thetaphi'])
            log.write('\nest GATEinput[\'emit\'] - ' + str(GATEinput['emit']) + '\n')
            log.write('           est emit_fac - ' + str(emit_fac) + '\n')

              #  kept exceeding *PI or zero so having to set a hard limits
            if emit_fac > 3.1415:
                emit_fac = 3.1415
                GATEinput['emit'] = GATEinput['sigXY']*GATEinput['thetaphi']*emit_fac
            if emit_fac < 0.5:
                emit_fac = 0.5
                GATEinput['emit'] = GATEinput['sigXY']*GATEinput['thetaphi']*emit_fac
            # if GATEinput['emit'] < 0.00001:
            #     GATEinput['emit'] = 0.00001
            #     emit_fac = GATEinput['emit']/(GATEinput['sigXY']*GATEinput['thetaphi'])

            log.write('\nnew GATEinput[\'emit\'] - ' + str(GATEinput['emit']) + '\n')
            log.write('           new emit_fac - ' + str(emit_fac) + '\n')
            log.write('\n\n\n' + '\n')

            # plt.close('all')  # need 'all' otherwise interferes with .wait() elsewhere
            plt.close('emi')
            plt.figure(num='emi')
            plt.scatter([_[1] for _ in emitt_record], [_[2] for _ in emitt_record], c=list(range(len(emitt_record))), cmap='Wistia')
            plt.title('Emittance:   ' + str(Etps))
            plt.plot([_[1] for _ in emitt_record], FITeqn([_[0] for _ in emitt_record]), '-')
            plt.plot([_[1] for _ in emitt_record], [TPSfit[2] for _ in emitt_record], '-')
            plt.plot(GATEinput['emit'], 0, 'o')
            plt.show(block=False)
            plt.pause(0.10)  # wait before next action for plt

            plt.close('fwhm')
            plt.figure(num='fwhm')
            plt.title('fwhm:  ' + str(Etps))
            plt.plot(TPSposition, TPS_profiles[Etps], 'o')
            plt.plot(position, fwhm_record[-1], '-')
            # plt.pause(10)  # wait before next action for plt
            plt.show(block=False)
            plt.pause(0.10)  # wait before next action for plt
        '''

        '''
        ###  print the fits to track during testing and to monitor process
        log.write()
        log.write('demonstrating the fitting for new values')
        log.write('             [   old       guess      current]')
        log.write('fitting for sigXY')
        log.write('     FWHM:  ' + str(['{:0.5f}'.format(_) for _ in [sigma_record[-2][1], 0.5*TPSeqn(TPSposition[0]), sigma_record[-1][1]]])
        log.write('    sigXY:  ' + str(['{:0.5f}'.format(_) for _ in [sigma_record[-2][0], newSigXY, sigma_record[-1][0]]])
        log.write('fitting for ThetaPhi')
        log.write('fit slope:  ' + str(['{:0.5f}'.format(_) for _ in [theta_record[-2][1], TPSfit[1], theta_record[-2][1]]])
        log.write(' ThetaPhi:  ' + str(['{:0.5f}'.format(_) for _ in [theta_record[-2][0], newThetaphi, theta_record[-1][0]]])
        log.write('fitting for Emittance')
        log.write('fit curve:  ' + str(['{:0.5e}'.format(_) for _ in [emitt_record[-2][1], TPSfit[2], emitt_record[-2][1]]])
        log.write('Emittance:  ' + str(['{:0.5f}'.format(_) for _ in [emitt_record[-2][0], newEmitt_fac, emitt_record[-1][0]]])

        ###  update the "new" values for GATE input
        GATEinput['sigXY'] = newSigXY
        '''


        log.write('\n\n\n' + '\n')
        log.write('###  END OF FULL ITERATION  ###\n' + '\n')
        log.write('New input values are - ' + '\n')
        log.write(str(GATEinput) + '\n')

        log.write('\n' + '\n')
        log.write(str(TPS_profiles[Etps]) + '\n')
        log.write(str([round(_,3) for _ in fwhm_record[-1]]) + '\n')
        log.write(str([round(fwhm_record[-1][_]-TPS_profiles[Etps][_],3) for _ in range(5)]) + '\n')
        log.write('\n')

        # plt.close('all')  # need 'all' otherwise interferes with .wait() elsewhere
        plt.close('tpi')
        plt.close('sig')
        # plt.close('emi')
        plt.close('fwhm')
        plt.close('fwhm_end')
        plt.figure(num='fwhm_end')
        plt.title('fwhm_end:  ' + str(Etps))
        plt.plot(TPSposition, TPS_profiles[Etps], 'o')
        plt.plot(position, fwhm_record[-1], '-')
        # plt.pause(10)  # wait before next action for plt
        plt.show(block=False)
        plt.pause(0.10)  # wait before next action for plt


        if all(abs(fwhm_record[-1][_]-TPS_profiles[Etps][_]) < 0.1 for _ in range(5)):
            break  #  wasn't respecting the criteria in while definition

    plt.close('all')
    log.write('\n\n\n\n\n' + '\n')
    log.write('###############################################################' + '\n')
    log.write('      CONVERGED' + '\n')
    log.write('              E_TPS:  ' + str(Etps) + '\n')
    log.write('Final GATE input is:  \n' + str(GATEinput) + '\n')
    log.write('\n')
    log.write('   TPS:  ' + str(TPS_profiles[Etps]) + '\n')
    log.write('    MC:  ' + str([round(_,3) for _ in fwhm_record[-1]]) + '\n')
    log.write('  diff:  ' + str([round(fwhm_record[-1][_]-TPS_profiles[Etps][_],3) for _ in range(5)]) + '\n')

    log.close()


    print('\n\n\n\n\n')
    print('###############################################################')
    print('      CONVERGED')
    print('              E_TPS:  ' + str(Etps))
    print('Final GATE input is:  \n', GATEinput)
    print()
    print('   TPS:  ', TPS_profiles[Etps])
    print('    MC:  ', [round(_,3) for _ in fwhm_record[-1]])
    print('  diff:  ', [round(fwhm_record[-1][_]-TPS_profiles[Etps][_],3) for _ in range(5)])





#############################################################################
#############################################################################
#############################################################################





###  The TPS data to be fit
TPS_energies = [70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 244]

# TPS_profiles={}
# for et,tpse in enumerate(TPS_energies):
#     TPS_profiles[tpse] = [plane1[et], plane2[et], plane3[et], plane4[et], plane5[et]]





#############################################################################
#############################################################################
#############################################################################





from multiprocessing import Pool, cpu_count
CPUpool = Pool(cpu_count())

to_match = []  #  orig = 36
matched = [70, 75, 80, 85, 90, 95, 100, 105, 110, 120, 130, 135, 140, 145, 150, 155, 160, 175, 195, 200, 225, 244]
# E_to_check = [85, 100, 120, 140, 180, 200, 220, 240]
E_to_check = [115, 125, 165, 170, 180, 185, 190, 205, 210, 215, 220, 230, 235, 240]


CPUpool.map(iterativeProfileFit, [etps for etps in TPS_energies if etps in E_to_check])





#############################################################################
#############################################################################
#############################################################################
















###  read in a template GATE macro to base calculations on
# import tkinter
# from tkinter import filedialog
# from os import path as osPath, chdir
# root = tkinter.Tk()
# root.withdraw()
# file = filedialog.askopenfilename(title='Please select the primary GATE macro')
# root.destroy()
#
# ###  direct to chosen file, used while debugging
# # from os import getcwd as getcwd
# # file = osPath.join(getcwd(),'MC-profile','characterize-beam-profile.mac')
#
# fPath, fName = osPath.split(file)[0], osPath.split(file)[1]
# chdir(fPath)


  #  this for loop will be what goes into the CPUpool above
  #  will parallelise fitting across energies
# for et,etps in enumerate(TPS_energies):
# for et,etps in enumerate(_ for _ in TPS_energies if _ in E_to_check):








'''

Final GATE input is:
 'ene': 69.39451918040326,
 'disp': 1.0808185890488056,
 'sigXY': 4.65057579094011,
 'thetaphi': 7.901745621079193,
 'emit': 115.4427955398292,
 'focus': 'positive',




first "working" iteration only on sigXY

Final GATE input is:   {
'ene': 69.39451918040326,
'disp': 1.0808185890488056,
'sigXY': 4.368047231518278,
'thetaphi': 10.33064955648,
'emit': 141.75944985999195,
'focus': 'positive',
'filePath': '/home/gate/coding/monteCarlo/MC-profile', 'fileName': 'characterize-beam-profile.mac'}





2nd seemingly working got the thetaphi almost perfect but sigmaXY was off
then I was a moron and hit ctrl-c to copy this text and stopped the run

demonstrating the fitting for new values
             [   old       guess      current]
fitting for sigXY
     FWHM:   ['7.91231', '4.95691', '4.46502']
    sigXY:   ['5.20094', '4.25710', '4.08643']
fitting for ThetaPhi
fit slope:   ['0.01689', '0.01227', '0.01258']
 ThetaPhi:   ['7.49807', '7.80551', '7.84032']

New input values are -
     newSigXY:     4.257097217215981
  newThetaPhi:    7.805510001824421

329 - end of loop
[12.247, 13.246, 14.394, 15.697, 16.908]
[11.001, 11.972, 13.314, 14.509, 16.025]









New input values are -
    newSigXY:     4.39122375958197
 newThetaPhi:    7.620664906935303
newEmitt_fac:     3.1415
newEmittance:   105.12729674908576


329 - end of loop
[12.247, 13.246, 14.394, 15.697, 16.908]
[12.1, 12.773, 14.003, 15.411, 16.68]
[-0.147, -0.473, -0.391, -0.286, -0.228]

'''










'''  ###  OUTPUT



'''







'''
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
