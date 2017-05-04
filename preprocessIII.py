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
import new_features
from datetime import date
from sklearn import preprocessing as pp

######################## BEGIN FUNCTION DEFINITIONS ########################

# helper function to format column names
def process_name(name):
  name = name.partition('(')[0]
  name = name.translate(None, '&-/')
  name = name.strip()
  return name.replace(' ', '_')


# helper function to create an arff file
def write_arff(file, col_names, data_matrix):

  # write header information
  file.write('@RELATION masshousingdata\n\n')
  for i, name in enumerate(col_names):
    if 'financial' not in name.lower():
      file.write('@ATTRIBUTE ')
      file.write(process_name(name))
      if 'raw' in name.lower():
        file.write(' STRING\n')
      else:
        file.write(' REAL\n')
  file.write('@ATTRIBUTE Financial_Rating {0, 1, 2, 3, 4}\n\n')

  # write data matrix
  file.write('@DATA\n')
  np.savetxt(file, data_matrix, fmt='%s', delimiter=',', newline='\n')

# helper function to process raw data
# takes a file pointer and returns the processed data matrix
# and a list of column names in order
def process_raw_data(data_file):
  today = date.today().toordinal()
  train_data = []
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
    #grade = cols[7].strip().upper() # letter grade is column 7
    #dsc = float(cols[8]) # dsc ratio is column 8
    #if grade != 'A' or 1.5 <= dsc and dsc <= 3.0:
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
        elif 'rm' in c_name and 'key' in c_name: # remove rm_key
          raw_rm_key_col.append([cols[i]])
        elif 'ratio' in c_name: # remove current ratio and dsc ratio
          pass
        else:
          row.append(np.nan if c_val == '' else c_val.replace(',',''))
      # convert all values to floating point numbers and append to data matrix
      train_data.append(map(float, row))

  # create numpy array from list object
  train_data_matrix = np.array(train_data)

  # impute missing values
  imputer = pp.Imputer(missing_values='NaN', strategy='mean', axis=0)
  train_data_matrix = imputer.fit_transform(train_data_matrix)

  # uncomment next two lines for standard feature scaling
  #std_scale = pp.StandardScaler().fit(train_data_matrix)
  #train_data_matrix = std_scale.transform(train_data_matrix)

  # uncomment next two lines for minmax feature normalization
  mean_scale = pp.MinMaxScaler().fit(train_data_matrix)
  train_data_matrix = mean_scale.transform(train_data_matrix)

  # add unscaled detail codes, grades, and raw data
  train_data_matrix = np.append(train_data_matrix, unscaled_detail_codes,axis=1)
  train_data_matrix = np.append(train_data_matrix, raw_rm_key_col, axis=1)
  train_data_matrix = np.append(train_data_matrix, raw_stmt_date_col, axis=1)
  train_data_matrix = np.append(train_data_matrix, grades, axis=1)

  # second, change column names to match data
  new_column_names = []
  for name in column_names:
      name = name.strip().lower()
      if 'date' in name:
        new_column_names.append(name.replace('date','days since').title())
      elif 'code' in name or 'grade' in name or 'ratio' in name:
        pass
      elif 'rm' in name and 'key' in name: # remove rm_key
        pass
      else:
        new_column_names.append(name.title())

  new_column_names.extend(['Is Detail Code_' + c for c in codes])
  new_column_names.append('Raw_Rm_Key')
  new_column_names.append('Raw_Stmt_Date')
  new_column_names.append('Financial_Rating')
  
  return train_data_matrix, new_column_names


######
# Preprocess function
# calling this function has the side effect of creating two
# output files: 1 training, 1 test
# 
# takes the name of the CSV files
######
def preprocess_csv(train_csv_name, test_csv_name, out_prefix):

  # try opening the files
  try:
    train_data_file = open(train_csv_name, 'r')
  except IOError as e:
    print 'ERROR: unable to find file', train_csv_name
    return

  try:
    test_data_file = open(test_csv_name, 'r')
  except IOError as e:
    print 'ERROR: unable to find file', test_csv_name
    return

  # read and process data
  try:
    train_data_matrix, train_column_names = process_raw_data(train_data_file)
    test_data_matrix, test_column_names = process_raw_data(test_data_file)
  finally:
    train_data_file.close()
    test_data_file.close()

  # open files for writing
  train_arffFile = open(out_prefix + '_train.arff', 'w')
  test_arffFile = open(out_prefix + '_test.arff', 'w')
  train_csvFile = open(out_prefix + '_train.csv', 'w')
  test_csvFile = open(out_prefix + '_test.csv', 'w')

  # create ARFF and CSV files from data
  try:

    # write column names as first line of csv files
    train_csvWriter = csv.writer(train_csvFile, dialect='excel')
    test_csvWriter = csv.writer(test_csvFile, dialect='excel')
    train_csvWriter.writerow(train_column_names)
    test_csvWriter.writerow(test_column_names)
    # write to CSVs
    np.savetxt(train_csvFile, train_data_matrix, fmt='%s', delimiter=',',\
                                                                   newline='\n')
    np.savetxt(test_csvFile, test_data_matrix, fmt='%s', delimiter=',',\
                                                                   newline='\n')

    # create train and test arff files
    write_arff(train_arffFile, train_column_names, train_data_matrix)
    write_arff(test_arffFile, test_column_names, test_data_matrix)

  finally:
    train_arffFile.close()
    test_arffFile.close()
    train_csvFile.close()
    test_csvFile.close()

######################### END FUNCTION DEFINITIONS #########################



########################## EXECUTE THIS SCRIPT DIRECTLY ######################

if __name__ == '__main__':

  new_train_in_name = new_features.getNewFeaturesAndFilename('TrainingData.csv')
  new_test_in_name = new_features.getNewFeaturesAndFilename('ExtraHousingData.csv')
  train_in_name = 'TrainingData.csv'
  test_in_name = 'ExtraHousingData.csv'
  out_name = 'housingdata'

  if len(sys.argv) < 2:
    print 'Using default input training csv file name:', new_train_in_name
  else:
    new_train_in_name = sys.argv[1].strip()
    
  if len(sys.argv) < 3:
    print 'Using default input testing csv file name:', new_test_in_name
  else:
    new_test_in_name = sys.argv[2].strip()
    
  if len(sys.argv) < 4:
    print 'Using default output file prefix:', out_name
  else:
    out_name = sys.argv[3].strip()

  preprocess_csv(new_train_in_name, new_test_in_name, out_name)
