# Converting text files generated by AIS DLK100A or ISEA potentiostats to simple csv readable by the KStat GUI

from glob import glob
import os
import pandas as pd

# create subdirectory
folder = 'converted'
if not os.path.isdir(folder):
    os.mkdir(folder)
    
# read list of files
files = glob("*")
files.remove('ConvertDLKtextToKStatCsv.py')
files.remove('converted')

for file in files:
    try:
        # find index of first data line:
        f = open(file, 'r')
        start = 0
        while True:
            line = f.readline()
            if 'Applied Potential' in line:
                break
            start = start + 1
        # read data file:
        df = pd.read_csv(file, skiprows = start+1, header = None, engine = 'python',
                         names=('potential', 'current'), delimiter = '\t\t\t')
        # invert current (KStat uses negative current, DLK positive)
        df. current = df.current*-1
        # convert potential to mV
        df. potential = df.potential *1000
        # save in subdirectory
        df.to_csv(folder+'/'+file+'.csv', index = False)
        print('Converted {}'.format(file))


    except Exception as e:
        print('Cannot convert file {}'.format(file))
        print(e)


