#!/usr/bin/env python

###############################################################################
#
# Preprocess the .csv file containing mass-housing raw data.
#
# COLUMNS USED FROM RAW DATA (1-BASED)
# STATIC: [1,6],[20,52]
# DYNAMIC: 7,[11,19]
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
  nyears = 5 # number of years in phase II training data
  today = date.today().toordinal()
  data = []
  tenth_year_grades = []
  unscaled_rm_key_col = []
  unscaled_stmt_year = []
  rm_map = {}
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
      elif 'ratio' in c_name: # ignore DSC Ratio and Current Ratio
        pass
      else:
        # replace missing values with NaN
        row.append(np.nan if c_val == '' else c_val.replace(',',''))
    # append row to list of rows associated with rm_key
    rm_key = int(row[0])
    if rm_key in rm_map:
      rm_map[rm_key].append(row)
    else:
      rm_map[rm_key] = [row]

  # reorganize data according to phase II scheme
  # CAUTION: MAGIC NUMBERS USED!
  for rm_key, rows in rm_map.iteritems():
    static_data = []
    if len(rows) >= 10:
      for i, val in enumerate(rows[0]): # append static data first
        if i <= 26 or i >= 38: # cols that have repeating data
          static_data.append(val)
    while len(rows) >= 10: # get first five years of data then remove year 1
      five_years_data = static_data[:]
      for row in rows[0:5]: # append changing data for first five years
        for i, val in enumerate(row):
          if i >= 27 and i <= 37 and i != 28: # changing data (except grade)
            five_years_data.append(val)
      data.append(map(float, five_years_data)) # append data to data matrix
      unscaled_rm_key_col.append([rows[9][0]]) # store original rm_key
      orig_date = date.fromordinal(today - rows[9][27])
      unscaled_stmt_year.append([orig_date.year]) # store stmt year
      tenth_year_grades.append([rows[9][28]]) # store letter grade
      del rows[0]

  # create numpy array from list object
  data_matrix = np.array(data)

  # impute missing values
  imputer = pp.Imputer(missing_values='NaN', strategy='mean', axis=0)
  data_matrix = imputer.fit_transform(data_matrix)

  # scale features
  data_matrix = pp.scale(data_matrix)

  # add unscaled columns and grade column last
  data_matrix = np.append(data_matrix, unscaled_rm_key_col, axis=1)
  data_matrix = np.append(data_matrix, unscaled_stmt_year, axis=1)
  data_matrix = np.append(data_matrix, tenth_year_grades, axis=1)

  # change column names to match data
  new_column_names = []
  tmp_col_names = []
  for name in column_names:
      name = process_name(name.strip().lower())
      if 'date' in name:
        tmp_col_names.append(name.replace('date','Days_Since').title())
      elif 'code' in name:
        tmp_col_names.extend(['Is_Detail_Code_' + c for c in codes])
      elif 'ratio' in name:
        pass
      else:
        tmp_col_names.append(name.title())

  # second pass to make col names match phase II specification
  new_column_names.extend(tmp_col_names[0:27]) # append static col names
  new_column_names.extend(tmp_col_names[38:]) # append static col names
  for i in xrange(nyears):
    for name in tmp_col_names[27:38]: # append dynamic cols
      if 'grade' not in name.lower(): # remove grade col
        new_column_names.append(name + '_Year_' + str(i + 1))

  new_column_names.append('Unprocessed_Rm_Key')
  new_column_names.append('Unprocessed_Stmt_Date')
  new_column_names.append('Financial_Grade_After_5_Years')
  
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

  # open file for writing
  arff = open(out_name, 'w')

  # create ARFF file from data
  try:
    arff.write('@RELATION masshousingdata\n\n')

    # column names
    for name in column_names:
      arff.write('@ATTRIBUTE ')
      if 'unprocessed' in name.lower():
        arff.write(name)
        arff.write(' STRING\n')
      elif 'grade' in name.lower():
        arff.write('class {A,B,C,D,F}\n')
      else:
        arff.write(name)
        arff.write(' REAL\n')
    arff.write('\n')

    # data matrix
    arff.write('@DATA\n')
    np.savetxt(arff, data_matrix, fmt='%s', delimiter=',', newline='\n')
  finally:
    arff.close()

  return data_matrix

######################### END FUNCTION DEFINITIONS #########################



########################## EXECUTE THIS SCRIPT DIRECTLY ######################

if __name__ == '__main__':

  in_name = 'TrainingData.csv'
  out_name = 'housingdata_train.arff'

  if len(sys.argv) < 2:
    print 'Using default input csv file name:', in_name
  else:
    in_name = sys.argv[1].strip()
    
  if len(sys.argv) < 3:
    print 'Using default output arff file name:', out_name
  else:
    out_name = sys.argv[2].strip()

  preprocess_csv(in_name, out_name)
