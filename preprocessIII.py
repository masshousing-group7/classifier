#!/usr/bin/env python

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
  unscaled_detail_codes = []
  raw_rm_key_col = []
  raw_stmt_date_col = []
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
        if 'stmt' in c_name:
          raw_stmt_date_col.append([cols[i]])
        mdy = c_val.split('/')
        d = date(int(mdy[2]), int(mdy[0]), int(mdy[1])).toordinal()
        row.append(today - d)
      elif 'code' in c_name: # handle detail code column
        detail_codes = []
        for code in codes:
          detail_codes.append(1 if c_val == code else 0)
        unscaled_detail_codes.append(detail_codes)
      elif 'grade' in c_name: # handle financial rating column
        if c_val == 'A':
          grades.append([0])
        elif c_val == 'B':
          grades.append([1])
        elif c_val == 'C':
          grades.append([2])
        elif c_val == 'D':
          grades.append([3])
        else:
          grades.append([4])
      else:
        if 'rm' in c_name and 'key' in c_name:
          raw_rm_key_col.append([cols[i]])
        row.append(np.nan if c_val == '' else c_val.replace(',',''))
    # convert all values to floating point numbers and append to data matrix
    data.append(map(float, row))

  # create numpy array from list object
  data_matrix = np.array(data)

  # impute missing values
  imputer = pp.Imputer(missing_values='NaN', strategy='mean', axis=0)
  data_matrix = imputer.fit_transform(data_matrix)

  # scale features (normalization)
  data_matrix = pp.scale(data_matrix)

  # add unscaled detail codes, grades, and raw data
  data_matrix = np.append(data_matrix, unscaled_detail_codes, axis=1)
  data_matrix = np.append(data_matrix, raw_rm_key_col, axis=1)
  data_matrix = np.append(data_matrix, raw_stmt_date_col, axis=1)
  data_matrix = np.append(data_matrix, grades, axis=1)

  # second, change column names to match data
  new_column_names = []
  for name in column_names:
      name = name.strip().lower()
      if 'date' in name:
        new_column_names.append(name.replace('date','days since').title())
      elif 'code' in name or 'grade' in name:
        pass
      else:
        new_column_names.append(name.title())

  new_column_names.extend(['Is Detail Code_' + c for c in codes])
  new_column_names.append('Unprocessed_Rm_Key')
  new_column_names.append('Unprocessed_Stmt_Date')
  
  return data_matrix, new_column_names


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
def preprocess_csv(csv_name, out_name):

  # open the file
  data_file = open(csv_name, 'r')

  # read and process data
  try:
    data_matrix, column_names = process_raw_data(data_file)
  finally:
    data_file.close()

  # open files for writing
  arffFile = open(out_name + '.arff', 'w')
  csvFile = open(out_name + '.csv', 'w')

  # create ARFF and CSV files from data
  try:
    # create CSV
    csvWriter = csv.writer(csvFile, dialect='excel')
    # uncomment next line to write column names to first line of csv file
    #csvWriter.writerow(column_names)
    np.savetxt(csvFile, data_matrix, fmt='%s', delimiter=',', newline='\n')

    # create ARFF
    arffFile.write('@RELATION masshousingdata\n\n')
    for i, name in enumerate(column_names):
      arffFile.write('@ATTRIBUTE ')
      arffFile.write(process_name(name))
      if 'unprocessed' in name.lower():
        arffFile.write(' STRING\n')
      else:
        arffFile.write(' REAL\n')
    arffFile.write('@ATTRIBUTE Financial_Rating {0, 1, 2, 3, 4}\n\n')

    # data matrix
    arffFile.write('@DATA\n')
    np.savetxt(arffFile, data_matrix, fmt='%s', delimiter=',', newline='\n')
  finally:
    arffFile.close()
    csvFile.close()

  return data_matrix

######################### END FUNCTION DEFINITIONS #########################



########################## EXECUTE THIS SCRIPT DIRECTLY ######################

if __name__ == '__main__':

  in_name = 'TrainingData.csv'
  out_name = 'housingdata_train'

  if len(sys.argv) < 2:
    print 'Using default input csv file name:', in_name
  else:
    in_name = sys.argv[1].strip()
    
  if len(sys.argv) < 3:
    print 'Using default output file name:', out_name
  else:
    out_name = sys.argv[2].strip()

  preprocess_csv(in_name, out_name)
