'''
###   programmes to supply file and/or directory paths

#  chooseDir() - supplies a directory location
                 Note:  requires user to navigate INTO the directory

#  chooseFile() - select a specific file, returns full path, filename, and dir

#  chooseOutFile() - define an output file location
                     uses chooseDir to pick a directory for the file
                     then prompts the user to define the output filename
'''







# usage:
# oPath = chooseDir(title='<optional message here>')

def chooseDir(title='Please navigate INTO desired directory'):

    import tkinter
    from tkinter import filedialog

    root = tkinter.Tk()
    dr = filedialog.askdirectory(title=title)
    root.destroy()

    return(dr)







# useage:
# if file == None:
#     file, fPath, fName = chooseFile()  # title='')
# else:
#     fPath, fName = osPath.split(file)[0], osPath.split(file)[1]
# # from os import chdir  #  optional
# # chdir(fPath)          #  optional

def chooseFile(title='Please select file'):

    import tkinter
    from tkinter import filedialog
    from os import path as osPath

    root = tkinter.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(title=title)
    root.destroy()
    fPath, fName = osPath.split(file)[0], osPath.split(file)[1]

    return(file, fPath, fName)







# useage:
# if oFile == None:
#     oFile, oPath, oName = chooseOutFile() # oPath=<directory>, oName=None)
# else:
#     fPath, fName = osPath.split(file)[0], osPath.split(file)[1]

def chooseOutFile(oPath=None, oName=None):

    from os import path as osPath
    from easygui import multenterbox

    if oPath == None:
        oPath = chooseDir()
    if oName == None:
        bxTitle = 'Output file'
        bxMsg = 'Please provide the output file location and name'
        bxOpts = ['file path', 'file name']
        oPath, oName = multenterbox(title=bxTitle, msg=bxMsg, fields=bxOpts, values=[oPath, oName])
    oFile = osPath.join(oPath, oName)

    return(oFile, oPath, oName)
