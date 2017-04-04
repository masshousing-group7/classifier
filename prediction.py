#####
#
#  Script uses a K Nearest Neighbor Classifier to predict a Finantial Rating Grade
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
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier, Evaluation, FilteredClassifier
from weka.core.classes import Random
from datetime import date
from weka.filters import Filter
from preprocess import preprocess_csv
from crossvalidation import cross_validate
from attribute_ranking import rank_attributes

# function to translate the grade
def get_grade(grade):
    if (grade == 1.0):
        return "GOOD"
    else:
        return "BAD"

# function for data classification with KNN
def classify_data_knn(data_set_train, data_set_test, neighbors_number):
    # load ARFF data set
    loader = Loader(classname="weka.core.converters.ArffLoader")
    
    # training dataset (uses housingdata_train.arff )
    train = loader.load_file(data_set_train)
    train.class_is_last()

    # immediately remove string attributes
    remove = Filter(classname='weka.filters.unsupervised.attribute.RemoveType',\
                                                       options=['-T', 'string'])
    remove.inputformat(train)
    no_strings = remove.filter(train)

    # testing dataset uses dataset, provided by TA
    #test = loader.load_file(data_set_test)
    #test.class_is_last()

	# build KNN classifier
    classifier = Classifier(classname='weka.classifiers.lazy.IBk', options=["-K", str(neighbors_number)])
    
    # here we set attributes that we want to remove to filter dataset
    # 73 and 74 - Unprocessed_Rm_Key and Unprocessed_Stmt_Date
    n = 10 # keep the top n features
    features = rank_attributes(no_strings)
    features = features[0:n]
    features.extend([75])
    feature_string = ','.join(map(str, features))
    print 'Feature indices removed:', feature_string
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove",\
                                      options=['-V', "-R", feature_string]) 

    # create a filtered classifier
    fc = FilteredClassifier()
    fc.filter = remove
    fc.classifier = classifier
    fc.build_classifier(train)

    # print false prediction to false_predictions.txt
    f = open('false_predictions.txt','w')
    #for index, inst in enumerate(test):
    for index, inst in enumerate(train):
        # predict the grade
        prediction = fc.classify_instance(inst)
        
        #if a predicted value doesn't match an actual grade
        if (inst.get_value(inst.class_index) != prediction):
            f.write(" Rm_key: " + str(inst.get_string_value(72)) +  
                    " Stmt_date: " + str(inst.get_string_value(73)) +
                    " expected grade: " + get_grade(inst.get_value(inst.class_index)) +
                    " predicted grade: " + get_grade(prediction) + '\n')
    f.close()

    # evaluate classifier	
    cross_validate(data_set_train, 5, neighbors_number)

# function to evaluate classifier and print some simple statistics
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
        # preprocess data
        # to generate new housing_train.arff uncomment the next line and provide 'MassHousingTrainData.csv'
        csv_name = 'TrainingData.csv'
        if len(sys.argv) > 1:
          csv_name = sys.argv[1].strip()
        preprocess_csv(csv_name, 'housingdata_train.arff')
        #preprocess_csv(csv_name, 'housingdata_test.arff') 
        
        # number of neighbors for KNN
        k = 3

        # classify data
        classify_data_knn('housingdata_train.arff', 'housingdata_test.arff', k)

    except Exception, e:
         print(traceback.format_exc())
    finally:
        jvm.stop()	

main()
