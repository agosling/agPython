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


###  Write out a DICOM file from the data stored in a DICOM data class
def dicomWrite(fullDCM=None, oFile=None, spotData=None, ifile=None):
    from easygui import buttonbox, fileopenbox



    #  select a template DICOM plan file to base output on
    tit = 'Select input DICOM file'
    msg = 'Select a template DICOM plan file\n\n\
            \tThis is more effective if exported from the patient and course\
              you intend to re-import your plan into.\n\
            \tPlan files are commonly of the format RN.*.*.*.dcm'
    if ifile is None:
        ifile = fileopenbox(title=tit, msg=msg, defaults='RN*.dcm'
                            filetypes=None, multiple=False)
    elif not file[-3:] is 'dcm':
        ifile = fileopenbox(title=tit, msg=msg, defaults='RN*.dcm'
                            filetypes=None, multiple=False)
    else:
        print('This module requires a template DICOM plan file to function')
        exit()



    #  Read in the DICOM file
    from pydicom.filereader import dcmread
    fullDCM = dcmread(ifile)



    #  if no dataset of spots supplied
    msg = 'Do you wish to overwrite existing plan with custom spots?'
    opt = ['Yes','No','Cancel']
    ans = buttonbox(title='Overwrite spots?', msg=msg, choices=opt)
    if ans is opt[2]:
        print('Cancel selected, exiting module'), exit()
    elif ans is opt[0]:
        try:
            from pbtMod import spotGenerator
            spotData = spotGenerator()
        else:
            print('This module requires the spotGenerator module\n\
                    This can be found at github.com/UCLHp/pbtMod')
            exit()



    #  select the output file location
    if oFile is None:
        from easygui import diropenbox
        msg = 'Choose the folder location to output the created DICOM files'
        oPath = diropenbox(title='Select output location', msg=None,\
                            default=osPath.split(ifile)[0])
        oFile = osPath.join(oPath, str(spotData.pName)+'.dcm')



    #  if selected, now replace the spot data
    if ans is opt[0]:

        #  adjusting the date and time of plan creation to now
        fullDCM.RTPlanLabel = spotData.pName  # (300a,0002)
        fullDCM.RTPlanDate = datetime.datetime.now().strftime('%Y%m%d')  # (300a,0006)
        fullDCM.RTPlanTime = datetime.datetime.now().strftime('%H%M%S.%f')  # (300a,0007)

        #  SOPInstanceUID is the unique identifier for each plan
        #  Final 2 sections are a generated ID number and date/time stamp
        sopInstUID = fullDCM.SOPInstanceUID.rsplit('.',2)
        fullDCM.SOPInstanceUID = sopInstUID[0] + '.' + str(randint(10000, 99999)) + '.' + fullDCM.RTPlanDate + fullDCM.RTPlanTime.rsplit('.')[0]

        #  ReferencedBeamNumber and BeamMeterset
        #  Need one for each beam in plan, so multiply if separating energy layers
        fullDCM.FractionGroupSequence[0].NumberOfBeams = spotData.numBeams
        # setting all elements in ReferencedBeam Sequence to same as 1st
        # to duplicate a class object and all elements within need copy.deepcopy
        # deepcopy ensures there isn't inheritance so changes to one doesn't affect others
        fullDCM.FractionGroupSequence[0].ReferencedBeamSequence = [deepcopy(fullDCM.FractionGroupSequence[0].ReferencedBeamSequence[0]) for _ in range(spotData.numBeams)]
        # now changing each BeamMeterset to sum of all sMeterset within beam
        for _ in range(spotData.numBeams):
            fullDCM.FractionGroupSequence[0].ReferencedBeamSequence[_].BeamMeterset = sum([sum(c.sMeterset) for c in spotData.beam[_].CP])
            fullDCM.FractionGroupSequence[0].ReferencedBeamSequence[_].ReferencedBeamNumber = _+1

        # need a PatientSetupSequence for each beam
        fullDCM.PatientSetupSequence = [deepcopy(fullDCM.PatientSetupSequence[0]) for _ in range(spotData.numBeams)]
        for _ in range(spotData.numBeams):
            fullDCM.PatientSetupSequence[_].PatientSetupNumber = _+1

        # The meat and potatoes of it all
        # have to create correct sized array of dicom structures before copying
        # https://stackoverflow.com/questions/28963354/typeerror-cant-pickle-generator-objects
        fullDCM.IonBeamSequence = [fullDCM.IonBeamSequence[0] for _ in range(spotData.numBeams)]
        # then use copy.deepcopy([]) to populate each time
        for b in range(spotData.numBeams):
            fullDCM.IonBeamSequence[b] = deepcopy(fullDCM.IonBeamSequence[0])

        for b in range(spotData.numBeams):
            fullDCM.IonBeamSequence[b].BeamNumber = b+1
            fullDCM.IonBeamSequence[b].BeamName = spotData.beam[b].bName + '-' + str(b+1)
            fullDCM.IonBeamSequence[b].FinalCumulativeMetersetWeight = sum([sum(c.sMeterset) for c in spotData.beam[b].CP])
            fullDCM.IonBeamSequence[b].NumberOfControlPoints = 2*spotData.beam[b].numCP
            # Here is where the Range Shifter data needs to be added if included - DO LATER
            # Creating Control Point entries
            # 2 for each position as need a 'start' and 'end for each point'
            fullDCM.IonBeamSequence[b].IonControlPointSequence = [fullDCM.IonBeamSequence[b].IonControlPointSequence[0], fullDCM.IonBeamSequence[b].IonControlPointSequence[1]]
            # again, need to use copy.deepcopy otherwise end up with inheritance!!!
            fullDCM.IonBeamSequence[b].IonControlPointSequence.extend([deepcopy(fullDCM.IonBeamSequence[b].IonControlPointSequence[1]) for _ in range(2*(spotData.beam[b].numCP-1))])
            # filling in the Control Point information
            # first control point in each beam contains additional data such as gantry angle etc.
            fullDCM.IonBeamSequence[b].IonControlPointSequence[0].GantryAngle = spotData.beam[b].gAngle
            fullDCM.IonBeamSequence[b].IonControlPointSequence[-1].CumulativeMetersetWeight = 0
            fullDCM.IonBeamSequence[b].IonControlPointSequence[0].CumulativeMetersetWeight = 0
            # fullDCM.IonBeamSequence[b].IonControlPointSequence[0].SnoutPosition
            # more range shifter settings
            # fullDCM.IonBeamSequence[b].IonControlPointSequence[0].Range Shifter Settings Sequence

            for c in range(0, 2*spotData.beam[b].numCP, 2):
                # Indexing
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ControlPointIndex = c
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].ControlPointIndex = c+1

                # number of spots used regularly enough to warrant for typing efficiency
                nSpots = len(spotData.beam[b].CP[c//2].X)

                # spot energies
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].NominalBeamEnergy = spotData.beam[b].CP[c//2].En
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].NominalBeamEnergy = spotData.beam[b].CP[c//2].En

                # number of spots at this energy
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].NumberOfScanSpotPositions = nSpots
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].NumberOfScanSpotPositions = nSpots

                # setting spot position map, is a list of x, y coordinates all together
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotPositionMap = [coord for pair in zip(spotData.beam[b].CP[c//2].X, spotData.beam[b].CP[c//2].Y) for coord in pair]
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].ScanSpotPositionMap = [coord for pair in zip(spotData.beam[b].CP[c//2].X, spotData.beam[b].CP[c//2].Y) for coord in pair]

                # Meterset weighting of each spot
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanSpotMetersetWeights = spotData.beam[b].CP[c//2].sMeterset
                # Meterset weight for every second CP is 0.0, acts as end point for each spot
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].ScanSpotMetersetWeights = [0.0 for _ in range(nSpots)]

                # the size of the spot at isocentre
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ScanningSpotSize = [spotData.beam[b].CP[c//2].sizeX, spotData.beam[b].CP[c//2].sizeY]
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].ScanningSpotSize = [spotData.beam[b].CP[c//2].sizeX, spotData.beam[b].CP[c//2].sizeY]

                # sum of previous control points
                # a CP with meterset listed doesn't add, the following with meterset 0.0 does add
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].CumulativeMetersetWeight = fullDCM.IonBeamSequence[b].IonControlPointSequence[c-1].CumulativeMetersetWeight
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].CumulativeMetersetWeight = fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].CumulativeMetersetWeight + sum(spotData.beam[b].CP[c//2].sMeterset)
                # and as a ratio of the total plane meterset
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c].ReferencedDoseReferenceSequence[0].CumulativeDoseReferenceCoefficient = fullDCM.IonBeamSequence[b].IonControlPointSequence[c].CumulativeMetersetWeight / fullDCM.IonBeamSequence[b].FinalCumulativeMetersetWeight
                fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].ReferencedDoseReferenceSequence[0].CumulativeDoseReferenceCoefficient = fullDCM.IonBeamSequence[b].IonControlPointSequence[c+1].CumulativeMetersetWeight / fullDCM.IonBeamSequence[b].FinalCumulativeMetersetWeight
            fullDCM.IonBeamSequence[b].ReferencedPatientSetupNumber = b+1



    #  write out the DICOM file
    fullDCM.save_as(oFile)






if __name__ == '__main__':
    dicomWrite()
