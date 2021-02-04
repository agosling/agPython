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







###  data is a list, each list element is a W2CADclass structure
  #  this allows for multiple entries into a single file
  #  data[0] should have any singular header information

def w2cadWrite(data=None, oFile=None):

    import datetime
    from easygui import filesavebox

    #  data present and format validation
    if not data:
        print('\nNo data supplied, why???')
        raise SystemExit()
    for dt in data:
        if dt.__class__.__name__ != 'W2CADdata':
            print('data in the wrong format to write out, exiting')
            exit()


    if not oFile:
        oFile = filesavebox(title='Select where to save the .w2cad file', \
                            msg=None, default='*', filetypes='*.w2cad')

    # use the data generated above to write the file
    with open(oFile, 'w') as of:

        #  file header information
        of.write('$ NUMS {:03d}\n'.format(len(data)))
        of.write('#\n# created by w2cadWrite.py\n# creation date: ' \
                  + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) \
                  + '\n#\n')

        #  for each entry in data, create an entry in the file
        for dt in data:
            of.write('$ STOM\n')
            for hd in dt.head:
                of.write('# '+str(hd)+'\n')
            for pm in dt.params:
                of.write('% '+str(pm)+'\n')
            for _ in range(len(dt.d)):
                of.write('< {x:+12.4f} {y:+12.4f} {z:+12.4f} {d:+12.4f} >\n'.format(x=dt.x[_], y=dt.y[_], z=dt.z[_], d=dt.d[_]))
            of.write('$ ENOM\n')
        of.write('$ ENOF\n')
