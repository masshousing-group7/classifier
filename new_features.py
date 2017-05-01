#####
#
#  In this file, I'm just containing methods to call create new features
#
####

import csv
import time

oldfile = ""
statements = {}
headers = []
newheaders = []
new_features = 
['change_housing_index',
 'perc_low_income',
 'perc_mod_income',
 'perc_market_rate',
 'perc_nonrevenue',
 'perc_elderly_restricted',
 'perc_unrestricted',
 'perc_student',
 'perc_other_restricted',
 'perc_fully_access_handi',
 'perc_part_access_handi',
 'perc_studio',
 'perc_1bed',
 'perc_2bed',
 'perc_3bed',
 'perc_4bed',
 'perc_5bed',
 'perc_6bed',
 'ratio_2bed_studio',
 'ratio_2bed_1bed',
 'ratio_2bed_3bed',
 'ratio_2bed_4bed',
 'ratio_2bed_5bed',
 'ratio_2bed_6bed',
]

# This next dict
# The yearly change in Massachusetts housing price index from FRED
# https://fred.stlouisfed.org/series/BOXRSA
home_price_index = {
    "1987": 0.392,
    "1988": 0.010,
    "1989": -0.142,
    "1990": -0.568,
    "1991": -0.198,
    "1992": 0.055,
    "1993": 0.171,
    "1994": 0.188
    "1995": 0.124
    "1996": 0.328
    "1997": 0.423
    "1998": 0.709
    "1999": 1.048
    "2000": 1.383
    "2001": 1.130
    "2002": 1.446
    "2003": 0.953
    "2004": 1.252
    "2005": 0.509
    "2006": -0.763
    "2007": -0.480
    "2008": -0.961
    "2009": 0.068
    "2010": -0.096
    "2011": -0.324
    "2012": 0.452
    "2013": 1.251
    "2014": 0.527
    "2015": 0.651
    "2016": 0.953
}


# Meaning that you want to run all the methods in this file and get the filename back
def getNewFeaturesAndFilename(csv_file):
    newcsvfile = ""

    csvToDict(csv_file)
    addNewFeatures()
    newcsvfile = dictToCSV(True)

    return newcsvfile


# Meaning that you want to run all the methods in this file and get the dictionary back
def getNewFeaturesAndDict(csv_file):
    csvToDict(csv_file)
    addNewFeatures()
    dictToCSV(False)
    return statements


def csvToDict(some_csv):
    global oldfile
    global headers
    global newheaders
    global statements

    oldfile = some_csv

    count = 0
    with open(some_csv) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if count == 0:
                headers.extend(row)  # This will be used to create the keys for the dict
                newheaders.extend(row)
            elif len(row) > 0:
                if count not in statements:  # Using the count as a dict key
                    statements[count] = {}  # Creates a dict for the id defined by count
                    for num in range(1, len(row)):
                        statements[count][headers[num]] = row[num]  # Ideally error check this
            count += 1

    # Now that we've got all the old ones, let's add some new ones!
    newheaders.extend(new_features)


def dictToCSV(boolval):
    global statements
    global headers
    global new_features
    global newheaders
    global oldfile

    timestamp = int(time.time())

    new_filename = str(timestamp) + ".newfeatures_" + oldfile = ".csv"
    with open (new_filename, 'w') as csvf:
        csvwriter = csv.writer(csvf, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(newheaders)

        for stmt in sorted(statements):
            tempRow = []
            for hdr in newheaders:
                tempRow.append(stmt[hdr])
            csvwriter.writerow(tempRow)

    if boolval is True:
        return new_filename
    elif boolval is False:
        return statements


def addNewFeatures():
    global statements
    global headers
    global new_features

    for feature in new_features:
        # Add some stuff
        # First add some housing index change info
        if 'change_housing_index' in feature:
            for sid in statements:
                if 'Stmt_date' in statements[sid].keys():
                    for year in home_price_index:
                        if year in statements[sid]['Stmt_date']:
                            statements[sid]['change_housing_index'] = home_price_index[year]
        elif 'perc_low_income' in feature:
            for sid in statements:
                temp = float(statements[sid]['Low Income Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_low_income'] = temp
        elif 'perc_mod_income' in feature:
            for sid in statements:
                temp = float(statements[sid]['Moderate Income Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_mod_income'] = temp
        elif 'perc_market_rate' in feature:
            for sid in statements:
                temp = float(statements[sid]['Market Rate Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_market_rate'] = temp
        elif 'perc_nonrevenue' in feature:
            for sid in statements:
                temp = float(statements[sid]['Non_revenue Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_nonrevenue'] = temp
        elif 'perc_elderly_restricted' in feature:
            for sid in statements:
                temp = float(statements[sid]['Elderly Restricted Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_elderly_restricted'] = temp
        elif 'perc_unrestricted' in feature:
            for sid in statements:
                temp = float(statements[sid]['Unrestricted Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_unrestricted'] = temp
        elif 'perc_student' in feature:
            for sid in statements:
                temp = float(statements[sid]['Student Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_student'] = temp
        elif 'perc_other_restricted' in feature:
            for sid in statements:
                temp = float(statements[sid]['Other Restricted Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_other_restricted'] = temp
        elif 'perc_fully_access_handi' in feature:
            for sid in statements:
                temp = float(statements[sid]['Fully Access Handicapped Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_fully_access_handi'] = temp
        elif 'perc_part_access_handi' in feature:
            for sid in statements:
                temp = float(statements[sid]['Partially Access Handicapped Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_part_access_handi'] = temp
        elif 'perc_studio' in feature:
            for sid in statements:
                temp = float(statements[sid]['Studio Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_studio'] = temp
        elif 'perc_1bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['One Bedroom Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_1bed'] = temp
        elif 'perc_2bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Two Bedroom Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_2bed'] = temp
        elif 'perc_3bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Three Bedroom Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_3bed'] = temp
        elif 'perc_4bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Four Bedroom Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_4bed'] = temp
        elif 'perc_5bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Five Bedroom Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_5bed'] = temp
        elif 'perc_6bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Six Bedroom Rental Units'])/float(statements[sid]['Total Rental Units'])
                statements[sid]['perc_6bed'] = temp
        elif 'ratio_2bed_studio' in feature:
            for sid in statements:
                temp = float(statements[sid]['Two Bedroom Rental Units'])/float(statements[sid]['Studio Rental Units'])
                statements[sid]['ratio_2bed_studio'] = temp
        elif 'ratio_2bed_1bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Two Bedroom Rental Units'])/float(statements[sid]['One Bedroom Rental Units'])
                statements[sid]['ratio_2bed_1bed'] = temp
        elif 'ratio_2bed_3bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Two Bedroom Rental Units'])/float(statements[sid]['Three Bedroom Rental Units'])
                statements[sid]['ratio_2bed_3bed'] = temp
        elif 'ratio_2bed_4bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Two Bedroom Rental Units'])/float(statements[sid]['Four Bedroom Rental Units'])
                statements[sid]['ratio_2bed_4bed'] = temp
        elif 'ratio_2bed_5bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Two Bedroom Rental Units'])/float(statements[sid]['Five Bedroom Rental Units'])
                statements[sid]['ratio_2bed_5bed'] = temp
        elif 'ratio_2bed_6bed' in feature:
            for sid in statements:
                temp = float(statements[sid]['Two Bedroom Rental Units'])/float(statements[sid]['Six Bedroom Rental Units'])
                statements[sid]['ratio_2bed_6bed'] = temp
        else:
            print("Unknown feature:  " + feature)

