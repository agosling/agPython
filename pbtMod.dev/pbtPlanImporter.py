import pydicom
import easygui as eg

'''
TLDR -  Code to run on DICOM plan files from Christie so they can be imported
        to Eclipse

This script has been created to facilitate the import of DICOM files from
the Christie. A few of the DICOM tags cause issues during import because they
have different names for machines/range shifters etc.
Note: The file is saved in place, so if you need to maintain the original -
only use this code on a COPY of the files sent from Manchester

Hex tags were used because I couldn't quite work out all the plain text tags
this is something I should fix in future, but for the time being I have
commented in the Tag names and what specifically is being changed
'''


def main():
    dicom_file = eg.fileopenbox()
    dicom_object = pydicom.read_file(dicom_file)
    # Change "Tolerance Table Label" to Physics
    dicom_object[0x300a, 0x03a0][0][0x300a, 0x43].value = 'Physics'
    # Change "Approval Status" to APPROVED
    dicom_object[0x300e, 0x2].value = 'APPROVED'

    # For each Beam in the "Ion Beam Sequence"
    for i in range(0, dicom_object[0x300a, 0x03a2].VM):
        # If the number of range shifters is not 0
        if dicom_object[0x300a, 0x03a2][i][0x300a, 0x312].value != 0:
            # Change the range shifter name to match our system
            dicom_object[0x300a, 0x03a2][i][0x300a, 0x314][0][0x300a, 0x318].value = 'RS = 5 cm'
        # Change the name of the machine to match our system
        dicom_object[0x300a, 0x03a2][i][0x300a, 0xb2].value = 'ProBeamDemoSPTC'
    # Save DICOM object
    dicom_object.save_as(dicom_file)


if __name__ == '__main__':
    main()
