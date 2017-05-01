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
# returns a mapping of rm_keys to their grade distributions
def count_grade_distribution(data_file):
  grade_dist = {}
  data_file.readline() # discard column names
  reader = csv.reader(data_file, dialect='excel')

  # iterate over raw data
  for cols in reader:
    rm_key = int(cols[0]) # rm key is column 0
    grade = cols[7].strip().upper() # letter grade is column 7
    if rm_key in grade_dist:
      if grade in grade_dist[rm_key]:
        grade_dist[rm_key][grade] += 1
      else:
        grade_dist[rm_key][grade] = 1
    else:
      grade_dist[rm_key] = {grade: 1}

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
    rm_keys = count_grade_distribution(train_data_file)
  except IOError as e:
    print 'Error occurred while opening or reading file', train_csv_name
    exit(1)

  five = {}
  four = {}
  three = {}
  two = {}
  one = {}
  for (key, grades) in rm_keys.iteritems():
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

  # uncoment this section to see grade distribution for selected rm_keys
  #validation_rm_keys = Set([769,774,1164,1048,786,660,792,1050,796,674,675,\
  #                          808,682,699,700,703,707,840,976,632,803,980,\
  #                          755,759,640,259,780,653,655,784,1042,771,789,\
  #                          783,805,992,749,1008,1143,766])

  #As = 0
  #Bs = 0
  #Cs = 0
  #Ds = 0
  #Fs = 0
  #for key in validation_rm_keys:
  #  for (k,v) in rm_keys[key].iteritems():
  #    if k == 'A':
  #      As += v
  #    elif k == 'B':
  #      Bs += v
  #    elif k == 'C':
  #      Cs += v
  #    elif k == 'D':
  #      Ds += v
  #    else:
  #      Fs += v

  #print 'As', As
  #print 'Bs', Bs
  #print 'Cs', Cs
  #print 'Ds', Ds
  #print 'Fs', Fs
  #exit(0)
  # end testing

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