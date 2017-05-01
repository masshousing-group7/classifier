#####
#
#  For phase I: function classify_data_knn
#  Script uses a K Nearest Neighbor Classifier to predict a Finantial Rating Grade
#  
#  For phase II: function classify_data
#  Script uses a MultiClassClassifier Classifier to predict a Finantial Rating Grade in 5 years
#
#  Uses housingdata_train.arff ( file generated by preprocess from original MassHousingTrainData.csv) to train the classifier
#  For testing this script uses housingdata_test.arff - file generated by preprocess from original csv, provided by TA
#  Script generates false_predictions.txt with false data predictions
#  
#  Usage: python prediction.py <csv Testing dataset>
#
####

import sys
import traceback
import os.path
import csv
import numpy as np
import weka.core.jvm as jvm
import weka.core.converters as converters
from weka.core.converters import Loader
import weka.core.dataset as ds
from weka.classifiers import Classifier, Evaluation, FilteredClassifier
from weka.core.dataset import Instances
from weka.core.dataset import Instance
from weka.core.dataset import Attribute
from weka.core.classes import Random
from datetime import date
from weka.filters import Filter, MultiFilter
#from preprocess import preprocess_csv #### for phase I for knn
from preprocessII import preprocess_csv
from attribute_ranking import rank_attributes
from splittrainingset import split_training_data

# function to translate the grade
def get_grade(grade):
    if (grade == 1.0):
        return "GOOD"
    else:
        return "BAD"

# function to translate the grade
def get_letter_grade(grade):
    if grade == 0.0:
        return "A"
    elif grade == 1.0:
        return "B"
    elif grade == 2.0:
        return "C"
    elif grade == 3.0:
        return "D"
    else:
        return "F"

#function for data classification for phase II with MultiClassClassifier and J48
def classify_data(data_set_train, data_set_test, output_file):
    loader = Loader("weka.core.converters.ArffLoader")
    
    # training dataset (uses housingdata_train.arff )
    train = loader.load_file(data_set_train)
    train.class_is_last()

    # testing dataset uses dataset, provided by TA
    test = loader.load_file(data_set_test)
    test.class_is_last()
      	
    remove = Filter(classname='weka.filters.unsupervised.attribute.RemoveType',\
                                                      options=['-T', 'string']) 
	
    # build a classifier
    classifier = Classifier(classname="weka.classifiers.meta.MultiClassClassifier")
    classifier.options=["-M","2","-W", "weka.classifiers.trees.J48","--", "-C","0.25","-B"]
    # build a filtered classifier
    fc = FilteredClassifier()
    fc.filter = remove
    fc.classifier = classifier
    fc.build_classifier(train)

    # print false prediction to false_predictions.txt
    f = open(output_file,'w')
    for index, inst in enumerate(test):
        # predict the grade
        prediction = fc.classify_instance(inst)
        dist = fc.distribution_for_instance(inst)
        
        #if a predicted value doesn't match an actual grade
        if (inst.get_value(inst.class_index) != prediction):
            f.write(" Rm_key: " + str(inst.get_string_value(69)) +  
                    " Stmt_year: " + str(inst.get_string_value(70)) +
                    " expected grade: " + get_letter_grade(inst.get_value(inst.class_index)) +
                    " predicted grade: " + get_letter_grade(prediction) +
                    " class distribution: " + str(dist)+'\n')
    f.close()

    # evaluate classifier	
    simple_evaluation(train, test, fc)
	
# function for data classification with KNN
def classify_data_knn(data_set_train, data_set_test, output_file, neighbors_number):
    loader = Loader("weka.core.converters.ArffLoader")
    
    # training dataset (uses housingdata_train.arff )
    train = loader.load_file(data_set_train)
    train.class_is_last()

    # testing dataset uses dataset, provided by TA
    test = loader.load_file(data_set_test)
    test.class_is_last()
      	
    remove = Filter(classname='weka.filters.unsupervised.attribute.RemoveType',\
                                                      options=['-T', 'string']) 
	
    # build a classifier
    classifier = Classifier(classname='weka.classifiers.lazy.IBk', options=["-K", str(neighbors_number)])
    # build a filtered classifier
    fc = FilteredClassifier()
    fc.filter = remove
    fc.classifier = classifier
    fc.build_classifier(train)

    # print false prediction to false_predictions.txt
    f = open(output_file,'w')
    for index, inst in enumerate(test):
        # predict the grade
        prediction = fc.classify_instance(inst)
        dist = fc.distribution_for_instance(inst)
        
        #if a predicted value doesn't match an actual grade
        if (inst.get_value(inst.class_index) != prediction):
            f.write(" Rm_key: " + str(inst.get_string_value(69)) +  
                    " Stmt_year: " + str(inst.get_string_value(70)) +
                    " expected grade: " + get_letter_grade(inst.get_value(inst.class_index)) +
                    " predicted grade: " + get_letter_grade(prediction) +
                    " class distribution: " + str(dist)+'\n')
    f.close()

    # evaluate classifier	
    simple_evaluation(train, test, fc)
	
def simple_evaluation(train_data_set, test_data_set, classifier):
    evaluation = Evaluation(train_data_set)
    evaluation.test_model(classifier, test_data_set)
	# print statistics
    print(evaluation.summary())
    print(evaluation.class_details())
    print(evaluation.matrix())	

# main function
def main():	
    try:
        jvm.start()
        print 'MultiClassClassifier with original training and testing datasets'
        classify_data('housingdata_train.arff', 'housingdata_test.arff', '1_MultiClass_false_predictions_phaseIII.txt')
        print 'MultiClassClassifier with produced training and testing datasets from original training dataset'
        classify_data("train_splitted.arff", "test_splitted.arff", '2_MultiClass_false_predictions_phaseIII.txt')
        print 'KNN Classifier with original training and testing datasets'
        classify_data_knn('housingdata_train.arff', 'housingdata_test.arff', '1_IBk_false_predictions_phaseIII.txt',1)
        print 'KNN Classifier with produced training and testing datasets from original training dataset'
        classify_data_knn("train_splitted.arff", "test_splitted.arff", '2_IBk_false_predictions_phaseIII.txt',1)
		
    except Exception, e:
         print(traceback.format_exc())
    finally:
        jvm.stop()	

main()