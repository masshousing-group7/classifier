#!/usr/bin/env python

###############################################################################
#
# Split the training set into training set and validation using a predetermined
# set of rm_keys.
#
# Usage: ./splittrainingset <in csv file path> <out arff file name>
# 
###############################################################################

import sys
import os.path
import csv
from sets import Set

######################## BEGIN FUNCTION DEFINITIONS ##########################

# helper function to split the training data into training and validation sets
# has the side effect of creating two arff files
def split_training_data(data_file, out_name_prefix):
  # selected rm keys based on count grade distribution script
  # using these keys for validation leaves us with 579 validation examples
  validation_rm_keys = Set([769,774,1164,1048,786,660,792,1050,796,674,675,\
                            808,682,699,700,703,707,840,976,632,803,980,\
                            755,759,640,259,780,653,655,784,1042,771,789,\
                            783,805,992,749,1008,1143,766])
  training_set = []
  validation_set = []
  column_names = data_file.readline().strip().split(',')
  reader = csv.reader(data_file, dialect='excel')

  # location index of rm_key
  rm_key_col = -1 # -1 causes an error if no key is found
  for (i, name) in enumerate(column_names):
    if 'rm' in name.lower() and 'key' in name.lower():
      rm_key_col = i
      break

  # iterate over data
  for cols in reader:
    if int(cols[rm_key_col]) in validation_rm_keys:
      validation_set.append(cols)
    else:
      training_set.append(cols)

  # try opening output arff files
  validation_out = out_name_prefix + '_validation.arff'
  train_out = out_name_prefix + '_train.arff'
  try:
    validation_file = open(validation_out, 'w')
    train_file = open(train_out, 'w')
    # write files here
  except IOError as e:
    print 'Error occurred writing files', validation_out, 'and', train_out

  return training_set, validation_set


######################### END FUNCTION DEFINITIONS #########################



########################## EXECUTE THIS SCRIPT DIRECTLY ######################

if __name__ == '__main__':

  if len(sys.argv) < 2:
    train_in_name = 'housingdata_train.csv'
  else:
    train_in_name = sys.argv[1].strip()

  if len(sys.argv) < 3:
    out_name = 'housingdata_train_split'
  else:
    out_name = sys.argv[2].strip()
    
  print 'Using input csv file name:', train_in_name
  print 'Using output arff file name:', out_name

  # try opening the input file
  try:
    train_data_file = open(train_in_name, 'r')
    train_set, validation_set = split_training_data(train_data_file, out_name)
  except IOError as e:
    print 'Error occurred while opening or reading file', train_csv_name
    exit(1)

  print 'Train Size:', len(train_set)
  print 'Validation Size:', len(validation_set)
