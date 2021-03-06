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

  total = float(all_As + all_Bs + all_Cs + all_Ds + all_Fs)
  print 'all_As', all_As, '({0:.2f}%)'.format(all_As / total * 100)
  print 'all_Bs', all_Bs, '({0:.2f}%)'.format(all_Bs / total * 100)
  print 'all_Cs', all_Cs, '({0:.2f}%)'.format(all_Cs / total * 100)
  print 'all_Ds', all_Ds, '({0:.2f}%)'.format(all_Ds / total * 100)
  print 'all_Fs', all_Fs, '({0:.2f}%)'.format(all_Fs / total * 100)
  print 'Total:', int(total)
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

  total = float(limited_As + limited_Bs + limited_Cs + limited_Ds + limited_Fs)
  print 'limited_As', limited_As, '({0:.2f}%)'.format(limited_As / total * 100)
  print 'limited_Bs', limited_Bs, '({0:.2f}%)'.format(limited_Bs / total * 100)
  print 'limited_Cs', limited_Cs, '({0:.2f}%)'.format(limited_Cs / total * 100)
  print 'limited_Ds', limited_Ds, '({0:.2f}%)'.format(limited_Ds / total * 100)
  print 'limited_Fs', limited_Fs, '({0:.2f}%)'.format(limited_Fs / total * 100)
  print 'Total:', int(total)
  print

  # selected rm_keys
  validation_rm_keys = Set([769,774,674,698,703,840,803,979,1002,1004,723,\
                            707,640,780,653,910,784,793,981,668,671,987,\
                            770,1067,1068,1072,645,1161,656,678,687,708,746,\
                            1052,938,823,957,1013,1059,715,1000,749])

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

  total = float(all_As + all_Bs + all_Cs + all_Ds + all_Fs)
  print 'all_As', all_As, '({0:.2f}%)'.format(all_As / total * 100)
  print 'all_Bs', all_Bs, '({0:.2f}%)'.format(all_Bs / total * 100)
  print 'all_Cs', all_Cs, '({0:.2f}%)'.format(all_Cs / total * 100)
  print 'all_Ds', all_Ds, '({0:.2f}%)'.format(all_Ds / total * 100)
  print 'all_Fs', all_Fs, '({0:.2f}%)'.format(all_Fs / total * 100)
  print 'Total:', int(total)
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

  total = float(limited_As + limited_Bs + limited_Cs + limited_Ds + limited_Fs)
  print 'limited_As', limited_As, '({0:.2f}%)'.format(limited_As / total * 100)
  print 'limited_Bs', limited_Bs, '({0:.2f}%)'.format(limited_Bs / total * 100)
  print 'limited_Cs', limited_Cs, '({0:.2f}%)'.format(limited_Cs / total * 100)
  print 'limited_Ds', limited_Ds, '({0:.2f}%)'.format(limited_Ds / total * 100)
  print 'limited_Fs', limited_Fs, '({0:.2f}%)'.format(limited_Fs / total * 100)
  print 'Total:', int(total)
  print
  # end selected rm_keys distribution in limited_rm_key set
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
