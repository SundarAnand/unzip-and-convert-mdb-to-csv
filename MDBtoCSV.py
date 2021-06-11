import os, sys, subprocess
import pandas as pd
import glob 
import zipfile

directory = "2019-08 Through 2020-03"

for filename in os.listdir(directory):
    if filename != ".DS_Store" and 'partial' not in filename:

        # Directories required for the  process
        inputdirname = directory + '/' + filename + '/'
        mdbdirectory = "mdb_files" + filename + '/'
        outdirectory = 'csv_files' + filename + '/' 

        # Extract zip files
        zipNames = glob.glob(inputdirname + '*.zip')
        for z in zipNames:
            archive = zipfile.ZipFile(z, 'r')
            archive.extractall(mdbdirectory)

        # Check the list of mdbfile generated
        mdbfilename = glob.glob(mdbdirectory + '*.mdb')

        # Generating CSV files from the .mdb files
        for dbName in mdbfilename:
            result = dbName.rpartition('-')
            print(result)
            prefix = result[0]
            table_names = subprocess.Popen(['mdb-tables', '-1', dbName], stdout=subprocess.PIPE).communicate()[0]
            tables = table_names.decode('UTF-8').split('\n')
            print(tables)
            for table in tables:
                if table != '':
                    filename = outdirectory + table.replace(' ','_') + '.csv'
                    with open(filename, 'wb') as f:
                        print('Exporting ' + filename)
                        subprocess.check_call(['mdb-export', dbName, table], stdout=f)