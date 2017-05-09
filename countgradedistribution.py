#!/usr/bin/env python

###############################################################################
#
# Count the grade distribution per rm_key in the raw housing data csv file
# and print to stdout.
#
# Usage: ./count_grade_distribution <csv file path>
# 
###############################################################################

import sys
import os.path
import csv
from sets import Set

######################## BEGIN FUNCTION DEFINITIONS ########################

# helper function to break down the grade distribution per rm key
# after limiting A observations to only those records with DSC
# ratio between 1.5 and 3.0 (inclusive)
def count_limited_distribution(data_file):
  lower = 1.5
  upper = 3.0
  grade_dist = {}
  data_file.readline() # discard column names
  reader = csv.reader(data_file, dialect='excel')

  # iterate over raw data
  for cols in reader:
    rm_key = int(cols[0]) # rm key is column 0
    grade = cols[7].strip().upper() # letter grade is column 7
    dsc = float(cols[8]) # dsc ratio is column 8
    if grade == 'A':
      if lower <= dsc and dsc <= upper:
        if rm_key not in grade_dist:
          grade_dist[rm_key] = {grade: 1}
        elif grade not in grade_dist[rm_key]:
          grade_dist[rm_key][grade] = 1
        else:
          grade_dist[rm_key][grade] += 1
      else: # ignore A records outside our range
        pass
    else:
      if rm_key not in grade_dist:
        grade_dist[rm_key] = {grade: 1}
      elif grade not in grade_dist[rm_key]:
        grade_dist[rm_key][grade] = 1
      else:
        grade_dist[rm_key][grade] += 1

  return grade_dist


# helper function to break down the grade distribution per rm key
# returns a mapping of rm_keys to their grade distributions
def count_grade_distribution(data_file):
  grade_dist = {}
  data_file.readline() # discard column names
  reader = csv.reader(data_file, dialect='excel')

  # iterate over raw data
  for cols in reader:
    rm_key = int(cols[0]) # rm key is column 0
    grade = cols[7].strip().upper() # letter grade is column 7
    if rm_key not in grade_dist:
      grade_dist[rm_key] = {grade: 1}
    elif grade not in grade_dist[rm_key]:
      grade_dist[rm_key][grade] = 1
    else:
      grade_dist[rm_key][grade] += 1

  return grade_dist


######################### END FUNCTION DEFINITIONS #########################



########################## EXECUTE THIS SCRIPT DIRECTLY ######################

if __name__ == '__main__':

  if len(sys.argv) < 2:
    train_in_name = 'TrainingData.csv'
  else:
    train_in_name = sys.argv[1].strip()
    
  print 'Using csv file name:', train_in_name

  # try opening the file
  try:
    train_data_file = open(train_in_name, 'r')
    all_rm_keys = count_grade_distribution(train_data_file)
    # 'rewind' file here
    train_data_file.seek(0)
    limited_rm_keys = count_limited_distribution(train_data_file)
  except IOError as e:
    print 'Error occurred while opening or reading file', train_csv_name
    exit(1)

  # tally grades in all_rm_key set
  all_As = 0
  all_Bs = 0
  all_Cs = 0
  all_Ds = 0
  all_Fs = 0
  print 'GRADE DISTRIBUTION IN ALL RM_KEYS'
  for (key, grades) in all_rm_keys.iteritems():
    for (k, v) in grades.iteritems():
      if k == 'A':
        all_As += v
      elif k == 'B':
        all_Bs += v
      elif k == 'C':
        all_Cs += v
      elif k == 'D':
        all_Ds += v
      else:
        all_Fs += v

  print 'all_As', all_As
  print 'all_Bs', all_Bs
  print 'all_Cs', all_Cs
  print 'all_Ds', all_Ds
  print 'all_Fs', all_Fs
  print

  # tally grades in limited_rm_key set
  limited_As = 0
  limited_Bs = 0
  limited_Cs = 0
  limited_Ds = 0
  limited_Fs = 0
  print 'GRADE DISTRIBUTION IN LIMITED RM_KEYS'
  for (key, grades) in limited_rm_keys.iteritems():
    for (k, v) in grades.iteritems():
      if k == 'A':
        limited_As += v
      elif k == 'B':
        limited_Bs += v
      elif k == 'C':
        limited_Cs += v
      elif k == 'D':
        limited_Ds += v
      else:
        limited_Fs += v

  print 'limited_As', limited_As
  print 'limited_Bs', limited_Bs
  print 'limited_Cs', limited_Cs
  print 'limited_Ds', limited_Ds
  print 'limited_Fs', limited_Fs
  print

  # selected rm_keys
  validation_rm_keys = Set([769,774,1164,1048,786,660,792,1050,796,674,675,\
                            808,682,699,700,703,707,840,976,632,803,980,\
                            979,993,955,744,1002,1004,\
                            755,759,640,259,780,653,784,1042,771,789,\
                            793,981,667,1057,938,684,823,712,972,720,\
                            783,805,992,749,1008,1143,766])

  # uncoment this section to see grade distribution for selected rm_keys in
  # all_rm_key set
  all_As = 0
  all_Bs = 0
  all_Cs = 0
  all_Ds = 0
  all_Fs = 0
  print 'GRADE DISTRIBUTION FOR SELECTED KEYS IN ALL_RM_KEY SET'
  for key in validation_rm_keys:
    for (k,v) in all_rm_keys[key].iteritems():
      if k == 'A':
        all_As += v
      elif k == 'B':
        all_Bs += v
      elif k == 'C':
        all_Cs += v
      elif k == 'D':
        all_Ds += v
      else:
        all_Fs += v

  print 'all_As', all_As
  print 'all_Bs', all_Bs
  print 'all_Cs', all_Cs
  print 'all_Ds', all_Ds
  print 'all_Fs', all_Fs
  print
  # end selected rm_keys distribution in all_rm_key set

  # uncoment this section to see grade distribution for selected rm_keys in
  # limited_rm_key set
  limited_As = 0
  limited_Bs = 0
  limited_Cs = 0
  limited_Ds = 0
  limited_Fs = 0
  print 'GRADE DISTRIBUTION FOR SELECTED KEYS IN LIMITED_RM_KEY SET'
  for key in validation_rm_keys:
    for (k,v) in limited_rm_keys[key].iteritems():
      if k == 'A':
        limited_As += v
      elif k == 'B':
        limited_Bs += v
      elif k == 'C':
        limited_Cs += v
      elif k == 'D':
        limited_Ds += v
      else:
        limited_Fs += v

  print 'limited_As', limited_As
  print 'limited_Bs', limited_Bs
  print 'limited_Cs', limited_Cs
  print 'limited_Ds', limited_Ds
  print 'limited_Fs', limited_Fs
  # end selected rm_keys distribution in limited_rm_key set
  print
  print 'Total:', limited_As + limited_Bs + limited_Cs + limited_Ds + limited_Fs
  exit(0)

  # this section prints the grade distrubtion for each rm_key
  # in a given set (either the limited set or over all rm_keys)
  # uncomment to print distribution for each rm_key
  print
  five = {}
  four = {}
  three = {}
  two = {}
  one = {}
  # uncomment for grade distribution of selected rm_keys
  # in all_rm_key set
  for (key, grades) in all_rm_keys.iteritems():
  # uncomment for grade distribution of selected rm_keys
  # in limited_rm_key set
  #for (key, grades) in limited_rm_keys.iteritems():
    if len(grades) == 5:
      five[key] = grades
    elif len(grades) == 4:
      four[key] = grades
    elif len(grades) == 3:
      three[key] = grades
    elif len(grades) == 2:
      two[key] = grades
    else:
      one[key] = grades
  
  print '================= KEYS WITH FIVE GRADES ================='
  for (key, grades) in five.iteritems():
    total = 0
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
      total += count
    print 'TOTAL:', total
  print
  print 'TOTAL KEYS:', len(five)
  print

  print '================= KEYS WITH FOUR GRADES ================='
  for (key, grades) in four.iteritems():
    total = 0
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
      total += count
    print 'TOTAL:', total
  print
  print 'TOTAL KEYS:', len(four)
  print

  print '================= KEYS WITH THREE GRADES ================='
  for (key, grades) in three.iteritems():
    total = 0
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
      total += count
    print 'TOTAL:', total
  print
  print 'TOTAL KEYS:', len(three)
  print

  print '================= KEYS WITH TWO GRADES ================='
  for (key, grades) in two.iteritems():
    total = 0
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
      total += count
    print 'TOTAL:', total
  print
  print 'TOTAL KEYS:', len(two)
  print

  print '================= KEYS WITH ONE GRADE ================='
  for (key, grades) in one.iteritems():
    total = 0
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
      total += count
    print 'TOTAL:', total
  print
  print 'TOTAL KEYS:', len(one)
