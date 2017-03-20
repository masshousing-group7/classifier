###############################################################################
#
# Preprocess the .csv file containing mass-housing raw data.
#
# Usage: ./preprocess <csv file path>
# 
###############################################################################

import sys
import os.path
import csv
import numpy as np
from datetime import date
from sklearn import preprocessing as pp

######
# Preprocess function
# calling this function has the side effect of creating an ARFF file
# named "housingdata.arff"
# 
# takes the name of the CSV file
#
# returns a numpy array of scaled features where the last column is the
# grade (0 or 1)
######
def preprocess_csv(csv_name):

  ######################## BEGIN FUNCTION DEFINITIONS ########################

  # helper function to format column names
  def process_name(name):
    name = name.partition('(')[0]
    name = name.translate(None, '&-/')
    name = name.strip()
    return name.replace(' ', '_')

  # helper function to process raw data
  # takes a file pointer and returns the processed data matrix
  # and a list of column names in order
  def process_raw_data(data_file):
    today = date.today().toordinal()
    data = []
    grades = []
    column_names = data_file.readline().strip().split(',')
    reader = csv.reader(data_file, dialect='excel')

    # 22 possible codes for detail code column
    codes = ['236DEC','DISPA','ELDER','INTERN','M2W','M2WDEC','MISC',\
              'OPTION','OSDEBT','RAD','RADDEC','RDAL','S8LMSA','S8NCON',\
              'S8SUBR','SEC13A','SEC236','SHARP','SHRDAL','SOFT','TCRED4',\
              'TCRED9']

    # first, build matrix of floating point values from raw data
    for cols in reader:
      row = []
      for i in xrange(len(cols)):
        c_name = column_names[i].strip().lower()
        c_val = cols[i].strip().upper()
        if 'date' in c_name: # handle date column
          mdy = c_val.split('/')
          d = date(int(mdy[2]), int(mdy[0]), int(mdy[1])).toordinal()
          row.append(today - d)
        elif 'code' in c_name: # handle detail code column
          for code in codes:
            row.append(1 if c_val == code else 0)
        elif 'grade' in c_name: # handle financial rating column
          grades.append([1 if (c_val == 'A' or
                               c_val == 'B' or
                               c_val == 'C') else 0])
        else:
          row.append(0 if c_val == '' else c_val.replace(',',''))
      # convert all values to floating point numbers and append to data matrix
      data.append(map(float, row))

    # create numpy array from list object and scale features
    data_matrix = pp.scale(np.array(data))

    # add grade column last
    data_matrix = np.append(data_matrix, grades, axis=1)

    # second, change column names to match data
    new_column_names = []
    for name in column_names:
        name = name.strip().lower()
        if 'date' in name:
          new_column_names.append(name.replace('date','days since').title())
        elif 'code' in name:
          new_column_names.extend(['Is Detail Code_' + c for c in codes])
        elif 'grade' in name:
          pass
        else:
          new_column_names.append(name.title())
    
    return data_matrix, new_column_names

  ######################### END FUNCTION DEFINITIONS #########################

  # output file name
  out_name = 'housingdata_train.arff'

  # open the file
  data_file = open(csv_name, 'r')

  # read and process data
  try:
    data_matrix, column_names = process_raw_data(data_file)
  finally:
    data_file.close()

  # open file for writing
  arff = open(out_name, 'w')

  # create ARFF file from data
  try:
    arff.write('@RELATION masshousingdata\n\n')

    # column names
    for name in column_names:
      arff.write('@ATTRIBUTE ')
      arff.write(process_name(name))
      arff.write(' REAL\n')
    arff.write('@ATTRIBUTE Financial_Rating {0, 1}\n\n')

    # data matrix
    arff.write('@DATA\n')
    np.savetxt(arff, data_matrix, fmt='%1g', delimiter=',', newline='\n')
  finally:
    arff.close()

  return data_matrix
