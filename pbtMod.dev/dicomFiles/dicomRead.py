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





  # add python modules folder in OS sensitive fashion
from os import path as osPath
from sys import path as sysPath
# print(osPath.split(sysPath[0])[0])
sysPath.append(osPath.join(osPath.split(sysPath[0])[0],'packages'))


###  Read in a DICOM file into data constructs and return
def dicomRead(file=None):
    from easygui import fileopenbox
    from pydicom.filereader import dcmread

    if file is None:
        file = fileopenbox(msg='msg', title='title', default='*.dcm',
                            filetypes=None, multiple=False)
    elif not file[-3:] is 'dcm':
        file = fileopenbox(msg='msg', title='title', default=file+'*.dcm',
                            filetypes=None, multiple=False)



    fullDCM = dcmread(file)



    ###  extracting the subset of dicom data desired
    from dataMod import PLANdata, BEAMdata, SPOTdata


    partDCM = PLANdata()
    partDCM.pName = fullDCM.RTPlanLabel
    partDCM.numBeams = fullDCM.FractionGroupSequence[0].NumberOfBeams
    # partDCM.numBeams = fullDCM[0x300a,0x70][0][0x300a,0x80].value

    # if some beams have been deleted, or re-arranged,
    # nBeams may not equal the numerical values that identify the beams
    # as the order varies within the file, best to use beam identifiers
    nB = [int(partDCM.numBeams)]
    for b in range(partDCM.numBeams):
        nB.append(int(fullDCM.IonBeamSequence[b].BeamNumber))


    partDCM.beam = [BEAMdata() for _ in range(max(nB))]
    for b in range(partDCM.numBeams):
        Bnum = fullDCM.IonBeamSequence[b].BeamNumber-1
        partDCM.beam[Bnum].bName = fullDCM.IonBeamSequence[b].BeamName
        partDCM.beam[Bnum].type = fullDCM.IonBeamSequence[b].TreatmentDeliveryType
        partDCM.beam[Bnum].bMetersetUnit = fullDCM.IonBeamSequence[b].PrimaryDosimeterUnit
        ''' to revert to full file read, remove '/2' when defining numCP and also see lower '''
        partDCM.beam[Bnum].numCP = int(fullDCM.IonBeamSequence[b].NumberOfControlPoints/2)
        # partDCM.beam[Bnum].numCP = fullDCM[0x300a,0x3a2][b][0x300a,0x110].value
    for b in range(partDCM.numBeams):
        Bnum = fullDCM.FractionGroupSequence[0].ReferencedBeamSequence[b].ReferencedBeamNumber-1
        if partDCM.beam[Bnum].type == 'TREATMENT':
            partDCM.beam[Bnum].bMeterset = fullDCM.FractionGroupSequence[0].ReferencedBeamSequence[b].BeamMeterset
            '''   working to here   '''
            print(partDCM.beam[Bnum].numCP)
            partDCM.beam[Bnum].CP = [SPOTdata() for _ in range(int(partDCM.beam[Bnum].numCP))]


    for b in range(partDCM.numBeams):
        Bnum = fullDCM.IonBeamSequence[b].BeamNumber-1
        if partDCM.beam[Bnum].type == 'TREATMENT':
            ''' to revert to full file read, remove *2 from numCP in range() and '/2' when incrementing CP lower down '''
            for c in range (2*partDCM.beam[Bnum].numCP):
                # if only single spot will be float, easier to convert to list
                if type(fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotMetersetWeights) is float:
                    fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotMetersetWeights = [fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotMetersetWeights]
                # excludes every second CP as don't contain any MU,
                # just a stop criterion for RTION files
                if fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotMetersetWeights[0] > 0.0:
                    partDCM.beam[Bnum].CP[int(c/2)].En = float(fullDCM.IonBeamSequence[b].IonControlPointSequence[c].NominalBeamEnergy)
                    for _ in range(0,len(fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotPositionMap),2):
                        partDCM.beam[Bnum].CP[int(c/2)].X.append(fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotPositionMap[_])
                        partDCM.beam[Bnum].CP[int(c/2)].Y.append(fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotPositionMap[_+1])
                    partDCM.beam[Bnum].CP[int(c/2)].sizeX = fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanningSpotSize[0]
                    partDCM.beam[Bnum].CP[int(c/2)].sizeY = fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanningSpotSize[1]
                    partDCM.beam[Bnum].CP[int(c/2)].sMeterset = fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotMetersetWeights
    return(fullDCM, partDCM)







if __name__ == '__main__':
    from os import getcwd
    f, p = dicomRead(file=getcwd())

    print(f)
    print('\n')
    print(p)

'''
###  from https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom_directory.html#sphx-glr-auto-examples-input-output-plot-read-dicom-directory-py

for patient_record in dicom_dir.patient_records:
    if (hasattr(patient_record, 'PatientID') and
            hasattr(patient_record, 'PatientName')):
        print("Patient: {}: {}".format(patient_record.PatientID,
                                       patient_record.PatientName))
'''
