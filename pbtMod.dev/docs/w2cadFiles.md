# w2cadFiles

## Scope

Handle the W2CAD file format used as input for the Varian Eclipse TPS

Able to read and write files of the correct format.

## Plan design

A data format in which the data is stored in a reasonable structure (a python class for easy passage between different functions.

A function to fit data into the defined class.

A function to read a file of w2cad format into the defined class.

A function to write out to a file in w2cad format if given data in the defined class.

## Elements

All stored in the sub-directory `w2cadFiles`

### projectFileName.py

**functionNameOne**

The details of functionNameOne

**functionNameTwo**

The details of functionNameTwo

## To Develop

Things to be added into the programme.

## Testing

Any testing to be performed and/or files included to test the fucntions.

## Issues

Things that are a problem that need to be updated and/or fixed.

# Appendix: DEV NOTES

## W2CAD file formats

This info is taken from the **Eclipse Protons Administration and Commissioning for ProBeam** document starting at p327 (in my personal version).

**_Overall structure is:_**<br>
Anything written between **...** is actually a comment here

```
$ NUMS 001   ** the number of measurements in the file **
$ STOM   ** start of the first measurement **
#
# ** some header information, whatever you wish to include **
#
% VERSION 02   ** this is fixed, do not change **
% DATE YYYY-MM-DD
% TYPE <some type>   ** there are very specific TYPE's, described below **
% ID <some ID>   ** ID of the TPS element the file must link to **
% AXIS X/Y/Z   *** chose one, tells system which column contains the x-axis **
< +000.00 -000.00 +000.00 -000.0>   ** the data, columns are X Y Z VALUE **
< +000.00 -000.00 +000.00 -000.0>
< +000.00 -000.00 +000.00 -000.0>
.
.
.
< +000.00 -000.00 +000.00 -000.0>
< +000.00 -000.00 +000.00 -000.0>
$ ENOM   ** end of the first measurement
$ STOM   ** start of the second measurement if present, repeat from STOM above **
.
.
.
$ ENOM   ** end of the second or last measurement **
$ ENOF   ** end of the file **
```

The types of `TYPE` include (all case sensitive):

- SingleWeT - Range Shifter
- BinaryWeT
- DiscreteWeT
- AnalogWeT
- Spacing_fSpotSize
- ZposSnout
- MeasuredSpotFluenceX/Y - used for spot profiles
- UserDefinedEffectiveSpotSizeX/Y - can give list of FWHM
- MeasuredDepthDose - for IDDs
- DDNormCorr - depth dose normalisation correction factor [1]
- DDNormFieldSizeCorrMS - depth dose normalisation for field size [2]
- etc...

[1] - Corrects MU/Gray for different size SOBP at different depths, columns are depths (in cm), rows are SOBP widths. [2] - fine tuning of the absolute dose for variable field sizes, columns are nominal energy (MeV), rows are number of spots in an energy layer
