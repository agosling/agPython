'''
###   displayMCoutput.py
#   used to quickly display the output from the monte carlo system
'''





from os import path as osPath
from sys import path as sysPath
sysPath.append(osPath.join(osPath.split( sysPath[0])[0],'packages'))
# print(sysPath)  # for debugging purposes



from easygui import buttonbox, multenterbox
from os import chdir
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



from fileOps import chooseFile
from fileOps import dataRead





def displayMCoutput(ftype=None, file=None, oFile=None, rng=None):


    if file == None:
        file, fPath, fName = chooseFile()
    else:
        fPath, fName = file.rsplit('/', 1)[0], file.rsplit('/', 1)[1]
    chdir(fPath)  #  optional


    bxChoice = ['Don\'t know', '1D data', '2D data']
    if ftype == None:
        bxTitle = 'Select MC file type'
        bxMsg = 'Select MC file type\n\nIDD data should select \'1D data\'\nDose planes should select \'2D data\''
        ftype = buttonbox(title=bxTitle, msg=bxMsg, choices=bxChoice, default_choice=bxChoice[0], cancel_choice=bxChoice[0])

    # if no selection or 'Don't know' selected then exit
    if ftype == bxChoice[0]:
        print('unknown file type, now exiting')
        exit()



    if ftype == '1D data':
        data = dataRead(file=file, param=['#', ' ', 'n', 'n'])
        d = [float(_[0]) for _ in data.row]
        x = list(range(0, len(d)))
        plt.plot(x, d)
        if(oFile!=None):
            plt.savefig(oFile, bbox_inches='tight')
            plt.clf()
        else:
            plt.show()
            plt.clf()


    elif ftype == '2D data':
        data = dataRead(file=file, param=['#', ' ', 'n', 'n'])
        d = np.array(data.col, dtype=float)
        min = np.min(d)
        max = np.max(d)
        mn = np.mean(d)
        md = np.median(d)
        sd = np.std(d)
        if rng == None:
            rmin, rmax = multenterbox(title='select display range', msg='choose range from:\n        \n   minimum:  '+str(min)+'        \n   maximum:  '+str(max)+'        \n      mean:  '+str(mn)+'        \n    median:  '+str(md)+'        \n   std dev:  '+str(sd)+'        \n  mean+3sd:  '+str(mn+3*sd)+'        \n  mean+5sd:  '+str(mn+5*sd)+'        \nmedian+3sd:  '+str(md+3*sd)+'        \nmedian+5sd:  '+str(md+5*sd), fields=['min', 'max'], values=[min, max])
        else:
            rmin, rmax = rng[0], md+rng[1]*sd
        rmin, rmax = (float(rmin), float(rmax))
        ax = sns.heatmap(d, vmin=rmin, vmax=rmax, cmap="gnuplot")
        if(oFile!=None):
            plt.savefig(oFile, bbox_inches='tight')
            plt.clf()
        else:
            plt.show()
            plt.clf()





if __name__ == '__main__':

    # displayMCoutput()

    ''
    bxTitle = 'Which programme?'
    bxMsg = 'Select the type of display you\'d like to perform'

    bxChoice = ['general display', 'all IDDs', 'all LET', 'Dose & LET']

    choice = buttonbox(title=bxTitle, msg=bxMsg, choices=bxChoice, default_choice=bxChoice[0], cancel_choice=bxChoice[0])

    if choice == bxChoice[0]:
        displayMCoutput()

    from fileOps import chooseDir
    from os import listdir
    from dataOps import basicSmooth, centralisedSmooth

    if choice == bxChoice[1]:
        oPath = chooseDir()
        iddFiles = [fl for fl in listdir(oPath) if 'doseIDD' in fl]
        # print(iddFiles)
        for id in iddFiles:
            data = dataRead(file=osPath.join(oPath,id), param=['#', ' ', 'n', 'n'])
            d = [float(_[0]) for _ in data.row]
            x = list(range(0, len(d)))
            plt.plot(x, d)
        plt.show()
        plt.clf()

    if choice == bxChoice[2]:
        oPath = chooseDir()
        iddFiles = [fl for fl in listdir(oPath) if 'LETIDD' in fl]
        # print(iddFiles)
        for id in iddFiles:
            data = dataRead(file=osPath.join(oPath,id), param=['#', ' ', 'n', 'n'])
            d = [float(_[0]) for _ in data.row]
            x = list(range(0, len(d)))
            # if want to smooth
            # d = basicSmooth(d, 20)
            # d = centralisedSmooth(d, 30)
            plt.plot(x, d)
        plt.show()
        plt.clf()

    if choice == bxChoice[3]:
        oPath = chooseDir()
        chdir(oPath)
        doseLETfiles = [fl for fl in listdir(oPath) if 'DoseToWater.txt' in fl]
        doseLETfiles = doseLETfiles + [fl for fl in listdir(oPath) if 'doseAveraged.txt' in fl]
        for df in doseLETfiles:
            data = dataRead(file=osPath.join(oPath,df), param=['#', ' ', 'n', 'n'])
            if 'IDD' in df:
                d = [float(_[0]) for _ in data.row]
                x = list(range(0, len(d)))
                plt.plot(x, d)
            if 'WCxz' in df:
                d = np.array(data.col, dtype=float)
                ax = sns.heatmap(d, cmap="gnuplot")
            plt.savefig(df.split('.')[0]+'.png', bbox_inches='tight')
            plt.clf()


    ''

'''

###  from https://scikit-image.org/docs/0.9.x/auto_examples/plot_circular_elliptical_hough_transform.html


Ellipse detection
=================

In this second example, the aim is to detect the edge of a coffee cup.
Basically, this is a projection of a circle, i.e. an ellipse.
The problem to solve is much more difficult because five parameters have to be
determined, instead of three for circles.


Algorithm overview
------------------

The algorithm takes two different points belonging to the ellipse. It assumes
that it is the main axis. A loop on all the other points determines how much
an ellipse passes to them. A good match corresponds to high accumulator values.

A full description of the algorithm can be found in reference [1]_.

References
----------
.. [1] Xie, Yonghong, and Qiang Ji. "A new efficient ellipse detection
       method." Pattern Recognition, 2002. Proceedings. 16th International
       Conference on. Vol. 2. IEEE, 2002
''

import matplotlib.pyplot as plt

from skimage import data, filter, color
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter

# Load picture, convert to grayscale and detect edges
image_rgb = data.coffee()[0:220, 160:420]
image_gray = color.rgb2gray(image_rgb)
edges = filter.canny(image_gray, sigma=2.0,
                     low_threshold=0.55, high_threshold=0.8)

# Perform a Hough Transform
# The accuracy corresponds to the bin size of a major axis.
# The value is chosen in order to get a single high accumulator.
# The threshold eliminates low accumulators
result = hough_ellipse(edges, accuracy=20, threshold=250,
                       min_size=100, max_size=120)
result.sort(order='accumulator')

# Estimated parameters for the ellipse
best = result[-1]
yc = int(best[1])
xc = int(best[2])
a = int(best[3])
b = int(best[4])
orientation = best[5]

# Draw the ellipse on the original image
cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
image_rgb[cy, cx] = (0, 0, 255)
# Draw the edge (white) and the resulting ellipse (red)
edges = color.gray2rgb(edges)
edges[cy, cx] = (250, 0, 0)

fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(10, 6))

ax1.set_title('Original picture')
ax1.imshow(image_rgb)

ax2.set_title('Edge (white) and result (red)')
ax2.imshow(edges)

plt.show()



###  another possible source of detection is:  https://photutils.readthedocs.io/en/stable/detection.html
'''
