import easygui as eg
from os import path as osPath



#  defaults is a pathway to begin search
#  filetypes is a list of file extensions



iFile = eg.fileopenbox(msg=None, title=None, default='*', \
                       filetypes=None, multiple=False)
#  can then split with
iPath, iName = osPath.split(iFile)[0], osPath.split(iFile)[1]



oFile = eg.filesavebox(msg=None, title=None, default='', filetypes=None)
oPath, oName = osPath.split(oFile)[0], osPath.split(oFile)[1]



dir = eg.diropenbox(msg=None, title=None, default=None)
