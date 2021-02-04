from multiprocessing import cpu_count
from subprocess import Popen as subprocessPopen
from os import path as osPath, remove as osRemove, chdir
from time import sleep as timeSleep
from psutil import cpu_percent
from random import shuffle





# nCPU = multiprocessing.cpu_count()
nCPU = cpu_count()
# print('nCPU = ', nCPU)





import tkinter
from tkinter import filedialog
root = tkinter.Tk()
root.withdraw()
file = filedialog.askopenfilename(title='Please select the primary GATE macro')
root.destroy()
fPath, fName = osPath.split(file)[0], osPath.split(file)[1]
chdir(fPath)





callGate = []





#############################################################################
###  Running the same Macro multiple times to speed up a simulation
def parallel_one():

    for c in range(1, nCPU, 1):
        callGate.append('\' ' + str(fName))
        # callGate.append('[ene,' + str(round(energy,3)) + '] [disp,' + str(round(dispersion,3)) + '] [sigXY,' + str(round(signaXY,3)) + '] [thetaphi,' + str(round(thetaPhi,3)) + '] [emit,' + str(round(em,3)) + '] [focus,' + str(focus) + ']\' ' + str(fName))
#############################################################################





#############################################################################
###  Variables for characterising the spot profiles for a single energy
  #  Use on the beam-character folder in projGATE
def char_profile():
    from math import sqrt

    # sigma and thetaphi up to 10 seems to cover full range
    E_TPS = [70, 100, 130, 160, 200, 240]
    sigmaXY  = [0.01]#, 0.1, 0.5, 1.0, 3.0, 7.0, 11.0, 15.0]#, 50.0, 100.0]
    thetaPhi = [0.1, 0.5, 1.0, 3.0, 7.0, 11.0, 15.0]#, 50.0, 100.0]
    emit_fac = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 3.1]
    focus = ['positive']#, 'negative']

    ###  convert given E_TPS energies into the matching MC energy and dispersion
    energy = [((0.0238/0.0222)*(E**1.75))**(1/1.77) for E in E_TPS]
    dispersion = [((-1*(0.2562232+(0.0034436*(((0.0238/0.0222)*(E**1.75))**(1/1.77)))))+sqrt((0.2562232+(0.0034436*(((0.0238/0.0222)*(E**1.75))**(1/1.77))))**2-(4*0.4117835*((0.0129581*(((0.0238/0.0222)*(E**1.75))**(1/1.77)))+(0.0000312*(((0.0238/0.0222)*(E**1.75))**(1/1.77))**2)-0.5333012-((0.0487*E)-(0.0000891*E**2)-1.44)))))/(2*0.4117835) for E in E_TPS]


    for e,en in enumerate(energy):
        for si in sigmaXY:
            for tp in thetaPhi:
                emit = [si*tp*_ for _ in emit_fac]
                for em in emit:
                    for fc in focus:
                        callGate.append('[ene,' + str(round(en,3)) + '] [disp,' + str(round(dispersion[e],3)) + '] [sigXY,' + str(round(si,3)) + '] [thetaphi,' + str(round(tp,3)) + '] [emit,' + str(round(em,5)) + '] [focus,' + str(fc) + ']\' ' + str(fName))
#############################################################################





if __name__ == '__main__':
    parallel_one()
    # char_profile()





    ''' may no longer be needed due to better CPU handling
    # check to see if the monitor file is present
    for c in range(1, nCPU, 1):
        print('checking for file:  output/gate.done.'+str(c)+'.txt\t')
        if osPath.isfile('output/gate.done.'+str(c)+'.txt'):
            print('termination file exists \n output/gate.done.'+str(c)+'.txt deleted at the start of the script')
            osRemove('output/gate.done.'+str(c)+'.txt')
    '''





    # initiate processes for the number of CPU - 1
    # need to keep one CPU/core free for basic OS operations
    print('\n   Initiating ' + str(len(callGate)) + ' processes across ' + str(nCPU-1) + ' CPU cores\n\n')

    # reset the counter to 0
    count = 0

    ###  initiates a process for all but 1 of the available CPUs
      #  this leaves one CPU to run system and other tasks otherwise
      #  the system is liable to freeze due to lack of resources

    while count < len(callGate):
        ###  monitoring CPU usage not just number of CPU
          #  https://stackoverflow.com/questions/6787684/how-to-capture-the-cpu-core-usage-from-system-monitor-program
          #  interval=XX is necessary as otherwise is instantaneous measure = 0
        cpuPercent = cpu_percent(interval=5, percpu=True)
          #  CPU with less than 75% load considered free for processes
        cpuFree = [cp+1 for cp,val in enumerate(cpuPercent) if val < 75.0]
        if not cpuFree:
            pass
        else:
            shuffle(cpuFree)
            cpuFree.pop()  #  leave a random core free
              #  for each free CPU...
            for cp in cpuFree:
                  #  generate the gate call command linked to that core
                callGate[count] = 'gate -a \'[n,' + str(cp) + '] ' + callGate[count] + ' > output/term-out-' + str(count+1) + '.txt &'
                  #  print to screen to track which process started
                print('[process ' + str(count+1) + ',  core ' + str(cp) + ']:  ' + str(callGate[count]))
                # run the gate execution command
                subprocessPopen(callGate[count], shell=True).wait()
                count += 1

    ### perhaps update to use multiprocessing.pool




























'''
for c in range(1, nCPU, 1):
    # create gate execution command
    callGate[count] = 'gate -a \'[n,' + str(c) + '] ' + callGate[count] + ' > output/term-out-' + str(count+1) + '.txt &'
    print('[process ' + str(count+1) + ',  core ' + str(c) + ']:  ' + str(callGate[count]))
    # run the gate execution command
    subprocessPopen(callGate[count], shell=True).wait()
    # leave time gap between starting processes
    # should hopefully mean finishes processes are caught
    count += 1
    timeSleep(10)

# print('count after first call:  ', count)  # for debugging purposes
# print('len(callGate):  ', len(callGate))  # for debugging purposes

process = []
while count < len(callGate):
    if len(process) > 0:
        # print('process:  ', process)  # for debugging purposes
        for p in process:
            callGate[count] = 'gate -a \'[n,' + str(p) + '] ' + callGate[count] + ' > output/term-out-' + str(count+1) + '.txt &'
            print('[process ' + str(count+1) + ',  core ' + str(p) + ']:  ' + str(callGate[count]))
            # run the gate execution command
            subprocessPopen(callGate[count], shell=True).wait()
            count += 1
        process = []

    else:
        # check for ended processes
        for c in range(1, nCPU, 1):
            if osPath.isfile('output/gate.done.'+str(c)+'.txt'):
                # note the process number to start
                process.append(c)
                # remove the file created when the process finished
                osRemove('output/gate.done.'+str(c)+'.txt')
        # add a time delay
        timeSleep(5)







# gate -a '[n,1] [sigXY,0.5] [thetaphi,0.5] [emit,0.125] [focus,positive]' characterize-beam-profile.mac > output/term-out-1.txt &
# gate -a '[n,2] [sigXY,0.5] [thetaphi,0.5] [emit,0.25] [focus,positive]' characterize-beam-profile.mac > output/term-out-2.txt &



###  Potential for developing the code further
###  https://medium.com/@urban_institute/using-multiprocessing-to-make-python-code-faster-23ea5ef996ba





''
###########################################################################
Script to Call an external program and wait.

This script is created to call an external program and wait - test version for
Gate

The responsibility to ensure that the outgoing plan does not have any error
that could affect any decision making remains with the user.


from subprocess import Popen as subprocessPopen
from os import path as osPath, remove as osRemove
from time import sleep as timeSleep

if osPath.isfile("output/gate.done.txt"):
    print("termination file exists \n output/gate.done.txt deleted at the start of the script")
    osRemove("output/gate.done.txt")

callGate = "Gate mac/proton.mac"

subprocessPopen(callGate, shell=True).wait()

print("finished calling Gate macro")

n = 0
while not osPath.exists("output/gate.done.txt"):
                n = n +1
                print("waiting loop " + str(n))
                timeSleep(30)

if osPath.isfile("output/gate.done.txt"):
    print("gate done next loop can be started")
###########################################################################

A touch on the mac file is that it has to have the following line in bold:

#############################################################################
# to check Steplimiter
#/tracking/verbose 1

/gate/application/noGlobalOutput
/gate/application/setTotalNumberOfPrimaries 100
/gate/application/start

/control/shell touch output/gate.done.txt

exit
#############################################################################
''






#############################################################################
# older code snippets removed
#############################################################################

'''
### when using separate folders for each cores output
'''
# check to see if the monitor file is present
for c in range(1, nCPU, 1):
    print('checking for file:  output'+str(c)+'/gate.done.txt\t')
    if osPath.isfile('output'+str(c)+'/gate.done.txt'):
        print('termination file exists \n output'+str(c)+'/gate.done.txt deleted at the start of the script')
        osRemove('output'+str(c)+'/gate.done.txt')
'''

'''
### previous attempt to step through and check for all the output
''
# for the remaining input parameter set
for _ in range(len(input_param)-count):
    if count < len(input_param):

        # check all output directories
        for c in range(1, nCPU, 1):
            # wait till process finished file is created
            while not osPath.exists('output'+str(c)+'/gate.done.txt'):
                timeSleep(5)

            # once process finished file is created
            if osPath.isfile('output'+str(c)+'/gate.done.txt'):
                # remove the file created when process finished
                osRemove('output'+str(c)+'/gate.done.txt')
                # create new gate execution command
                callGate = 'gate -a \'[run,' + str(c) + '] [size,' + str(input_param[count][0]) + '] [thetaphi,' + str(input_param[count][1]) + '] [emit,' + str(input_param[count][2]) + ']\' characterize-beam-profile.mac &' # > output' + str(c) + '/term-out-' + str(count+1) + '.txt &'
                count += 1
                print('[process ' + str(count) + ',  core ' + str(c) + ']:  ' + str(callGate))
                # run the gate execution command
                subprocessPopen(callGate, shell=True).wait()

'''
