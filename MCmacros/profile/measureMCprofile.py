from sys import path as sysPath
from os import path as osPath
sysPath.append(osPath.join(osPath.expanduser('~'),'packages'))


from os import chdir, remove
from multiprocessing import Pool, cpu_count
from subprocess import Popen as subprocessPopen
from monteCarlo import openMHD
import numpy as np
from dataMod import fitGaussian, fitLine



def genFitProfile(input=None):

    if not input:
        raise SystemExit

    ###  run the gate call command and wait for completion
    from subprocess import Popen as subprocessPopen
    subprocessPopen(input[0], shell=True).wait()

    ###  own function to read in an MHD file using SimpleITK
    from monteCarlo import openMHD
    (size, spacing, dosecube) = openMHD(file=input[1])

      #  collapse 3D dose cube in Y-direction to get X-Z plane
    import numpy as np
    dose2d = np.sum(dosecube, axis=1)
      #  create an array of the X positions for each pixel
    axis = np.array([_*spacing[2] for _ in range(np.shape(dose2d)[1])])

    ###  measure the gaussian profile of the beam at every depth
    from dataMod import fitGaussian
    beam = []
    for depth in range(np.shape(dose2d)[0]):
        doseProfile = dose2d[depth]
        (fit, _, fwhm) = fitGaussian(axis, doseProfile, init=[1,50,1])
          #  VERY IMPORTANT to have a good init value - was failing without

        beam.append([depth*spacing[0], fit[1], fwhm])

    ###  2nd and 3rd order fits to the fwhm curves with depth
    from dataMod import fitLine
    (soln2, func2) = fitLine(dataX=[_[0] for _ in beam],
                            dataY=[_[2] for _ in beam], order=2)
    (soln3, func3) = fitLine(dataX=[_[0] for _ in beam],
                            dataY=[_[2] for _ in beam], order=3)

    ###  remove output files as they take up a lot of space
    from os import remove
    fileRoot = input[1].rsplit('.',1)[0]
    remove(fileRoot+'.mhd')
    remove(fileRoot+'.raw')
    remove(fileRoot+'-Squared.mhd')
    remove(fileRoot+'-Squared.raw')
    remove(fileRoot+'-Uncertainty.mhd')
    remove(fileRoot+'-Uncertainty.raw')

    print([soln2, func2, soln3, func3])
    return([soln2, func2, soln3, func3])





#############################################################################

def mcProfiles():

    ###  obtain the path to the GATE macro
    import easygui as eg
    file = eg.fileopenbox(title='select primary GATE macro', msg=None,
                          default=sysPath[0], filetypes='*.mac')
    ###  change into the gate macro file location
    from os import chdir
    chdir(osPath.split(file)[0])

    ###  the input values to be used
    ene = [70, 155, 245]  #  105, 140, 175, 210,
    dsp = [0.1, 1.0, 1.5]  #  0.5,
    sxy = [3.0, 4.0, 5.0]  #  3.5, 4.5,
    tpi = [0.001, 0.01, 0.1]  #  0.005, 0.05,
    fac = [2.5, 3.0, 3.14]  #  2.8, 3.1,
    emt = []
    fcs = ['positive']

    callGate = []
    outFiles = []
    settings = []

    for en in ene:
        for di in dsp:
            for si in sxy:
                for tp in tpi:
                    for fa in fac:
                        #  calculate an emittance value
                        em = si*tp*fa
                        for fc in fcs:
                            settings.append([en, di, si, tp, fa, em, fc])
                            callGate.append( 'gate -a \'[ene,'
                                            + str(round(en,3)) + '] [disp,'
                                            + str(round(di,3)) + '] [sigXY,'
                                            + str(round(si,3)) + '] [thetaphi,'
                                            + str(round(tp,3)) + '] [emit,'
                                            + str(round(em,5)) + '] [focus,'
                                            + str(fc) + ']\' '
                                            + str(osPath.split(file)[1])
                                            + ' > ' + str(osPath.join(
                                            osPath.split(file)[0],
                                            'output',
                                            'gateLog-'
                                            + str(round(en,3))+'-'
                                            + str(round(di,3))+'-'
                                            + str(round(si,3))+'-'
                                            + str(round(tp,3))+'-'
                                            + str(round(em,5))+'-'
                                            + str(fc)+'.txt'
                                            )))
                            outFiles.append(str(osPath.join(
                                            osPath.split(file)[0],
                                            'output',
                                            'doseVol-'+
                                            str(round(en,3))+'-'+
                                            str(round(di,3))+'-'+
                                            str(round(si,3))+'-'+
                                            str(round(tp,3))+'-'+
                                            str(round(em,5))+'-'+
                                            str(fc)+'-Dose.mhd'
                                            )))

    simput = [[callGate[_], outFiles[_]] for _,x in enumerate(callGate)]
    print(settings)
    # print(simput)

    from multiprocessing import Pool, cpu_count
    CPUpool = Pool(cpu_count())

    results = CPUpool.map(genFitProfile, [s for s in simput])

    for c in range(len(simput)):
        print(settings[c], results[c])



if __name__ == '__main__':
    # main([2,3])
    mcProfiles()

###  needs to send the gate output into a separate file for later inspection
###  needs to update on progress

'''

[70, 0.1, 3.0, 0.001, 2.5, 0.0075, 'positive'] [array([6.51064083e+00, 4.13469179e-03, 1.50519002e-07]), poly1d([1.50519002e-07, 4.13469179e-03, 6.51064083e+00]), array([ 7.66326783e+00, -2.80535745e-03,  8.83860978e-06, -2.89892919e-09]), poly1d([-2.89892919e-09,  8.83860978e-06, -2.80535745e-03,  7.66326783e+00])]

[70, 0.1, 3.0, 0.001, 2.5, 0.0075, 'positive'] [array([ 7.75640476e+00, -1.38781622e-03,  3.86662688e-06]), poly1d([ 3.86662688e-06, -1.38781622e-03,  7.75640476e+00]), array([ 7.77665048e+00, -1.50971713e-03,  4.01923188e-06, -5.09192520e-11]), poly1d([-5.09192520e-11,  4.01923188e-06, -1.50971713e-03,  7.77665048e+00])]
[70, 0.1, 3.0, 0.001, 2.8, 0.0084, 'positive'] [array([ 7.50162888e+00, -1.11308436e-03,  3.91962568e-06]), poly1d([ 3.91962568e-06, -1.11308436e-03,  7.50162888e+00]), array([ 7.56447350e+00, -1.49147634e-03,  4.39332605e-06, -1.58058180e-10]), poly1d([-1.58058180e-10,  4.39332605e-06, -1.49147634e-03,  7.56447350e+00])]
[70, 0.1, 3.0, 0.005, 2.5, 0.0375, 'positive'] [array([ 7.70166088e+00, -1.48185020e-03,  3.97528819e-06]), poly1d([ 3.97528819e-06, -1.48185020e-03,  7.70166088e+00]), array([ 7.69594265e+00, -1.44742031e-03,  3.93218620e-06,  1.43817129e-11]), poly1d([ 1.43817129e-11,  3.93218620e-06, -1.44742031e-03,  7.69594265e+00])]
[70, 0.1, 3.0, 0.005, 2.8, 0.041999999999999996, 'positive'] [array([ 7.66255551e+00, -1.53081037e-03,  3.99899916e-06]), poly1d([ 3.99899916e-06, -1.53081037e-03,  7.66255551e+00]), array([ 7.67377795e+00, -1.59838151e-03,  4.08358994e-06, -2.82251521e-11]), poly1d([-2.82251521e-11,  4.08358994e-06, -1.59838151e-03,  7.67377795e+00])]
[70, 0.1, 3.5, 0.001, 2.5, 0.00875, 'positive'] [array([ 9.03769519e+00, -1.96038848e-03,  4.20111976e-06]), poly1d([ 4.20111976e-06, -1.96038848e-03,  9.03769519e+00]), array([ 8.93353289e+00, -1.33321983e-03,  3.41598150e-06,  2.61974728e-10]), poly1d([ 2.61974728e-10,  3.41598150e-06, -1.33321983e-03,  8.93353289e+00])]
[70, 0.1, 3.5, 0.001, 2.8, 0.0098, 'positive'] [array([ 8.83729817e+00, -1.19524113e-03,  3.64098251e-06]), poly1d([ 3.64098251e-06, -1.19524113e-03,  8.83729817e+00]), array([ 8.89949931e+00, -1.56975864e-03,  4.10983253e-06, -1.56439777e-10]), poly1d([-1.56439777e-10,  4.10983253e-06, -1.56975864e-03,  8.89949931e+00])]
[70, 0.1, 3.5, 0.005, 2.5, 0.043750000000000004, 'positive'] [array([ 8.77025657e+00, -1.30069793e-03,  3.73605136e-06]), poly1d([ 3.73605136e-06, -1.30069793e-03,  8.77025657e+00]), array([ 8.66342730e+00, -6.57471325e-04,  2.93081051e-06,  2.68682299e-10]), poly1d([ 2.68682299e-10,  2.93081051e-06, -6.57471325e-04,  8.66342730e+00])]
[70, 0.1, 3.5, 0.005, 2.8, 0.049, 'positive'] [array([ 8.84042688e+00, -1.53776826e-03,  3.80668327e-06]), poly1d([ 3.80668327e-06, -1.53776826e-03,  8.84042688e+00]), array([ 8.74411826e+00, -9.57887169e-04,  3.08074324e-06,  2.42222232e-10]), poly1d([ 2.42222232e-10,  3.08074324e-06, -9.57887169e-04,  8.74411826e+00])]
[Finished in 1692.019s]
'''




'''  from development phase
import matplotlib.pyplot as plt
from dataMod import fitGaussian, centralisedSmooth, fitLine

    if 1 in v:
        # transverse view
        plt.imshow(np.sum(dosecube, axis=0), interpolation='bilinear')
        plt.show()
        #  beam axis (long) view
        plt.imshow(np.sum(dosecube, axis=1), interpolation='bilinear')
        plt.show()
        plt.imshow(np.sum(dosecube, axis=2), interpolation='bilinear')
        plt.show()


    dose2d = np.sum(dosecube, axis=1)
    axis = np.array([_*spacing[2] for _ in range(np.shape(dose2d)[1])])

    if 2 in v:

        ###  running for every step in depth
        beam = []
        for depth in range(np.shape(dose2d)[0]):
            doseProfile = dose2d[depth]
            (fit, _, fwhm) = fitGaussian(axis, doseProfile, init=[1,50,1])
              #  VERY IMPORTANT to have a good init value - was failing without

            beam.append([depth*spacing[0], fit[1], fwhm])

        plt.scatter([_[0] for _ in beam], [_[1] for _ in beam], s=1)
        plt.show()
        plt.scatter([_[0] for _ in beam], [_[2] for _ in beam], s=1)
        plt.show()

    if 3 in v:

        (soln1, func1) = fitLine(dataX=[_[0] for _ in beam],
                                dataY=[_[2] for _ in beam], order=1)
        (soln2, func2) = fitLine(dataX=[_[0] for _ in beam],
                                dataY=[_[2] for _ in beam], order=2)
        (soln3, func3) = fitLine(dataX=[_[0] for _ in beam],
                                dataY=[_[2] for _ in beam], order=3)

        print(soln1)
        print(soln2)
        print(soln3)

        plt.scatter([_[0] for _ in beam], [_[2] for _ in beam], s=1)
        # plt.plot([_[0] for _ in beam], func1([_[0] for _ in beam]))
        # plt.plot([_[0] for _ in beam], func2([_[0] for _ in beam]))
        plt.plot([_[0] for _ in beam], func3([_[0] for _ in beam]))
        plt.show()
'''
