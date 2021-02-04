# monteCarlo

GATE user guide:  [http://wiki.opengatecollaboration.org/index.php/Users_Guide](http://wiki.opengatecollaboration.org/index.php/Users_Guide)

## Aim

To setup an independent Monte Carlo dose calculation solution which simulates the output of the Varian ProBeam gantry as closely as possible. This will be used to re-calculate patient treatments as a secondary and independent dose check, and as part of the commissioning process.

## Outline

The solution will use the Geant4 Monte Carlo system as developed by CERN, with the GATE user interface.
Tasks will involve:

 - Characterisation of the treatment beam for all energies with and without the range shifter
 - A method to convert the treatment plans to input for the Monte Carlo system
 - Import of the CT and structure datasets to create a simulation "world"
 - Running of the simulation - to speed up the run time a server solution with multiple CPU cores will be used
 - Recording of the dose as calculated within the simulation and conversion back to a format readable in Eclipse

## Functionality



#### Development stages and notes


## Milestones

 - [ ] Beam on
 - [ ]

### Additional aspects for development

 - A 3D gamma analysis between the treatment planning system and Monte Carlo calculations
 - A second map of the dose-weighted LET as an RBE surrogate
