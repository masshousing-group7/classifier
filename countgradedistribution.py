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
    print 'Error occurred while opening or readin file', train_csv_name
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

  print '================= KEYS WITH FIVE GRADES ================='
  for (key, grades) in five.iteritems():
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
  print

  print '================= KEYS WITH FOUR GRADES ================='
  for (key, grades) in four.iteritems():
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
  print

  print '================= KEYS WITH THREE GRADES ================='
  for (key, grades) in three.iteritems():
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
  print

  print '================= KEYS WITH TWO GRADES ================='
  for (key, grades) in two.iteritems():
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
  print

  print '================= KEYS WITH ONE GRADE ================='
  for (key, grades) in one.iteritems():
    print 'RM KEY:', key
    for (grade, count) in grades.iteritems():
      print grade, ':', count
  print
