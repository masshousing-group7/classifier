######
#
#  Script performs 5 - fold - cross - validation for KNN classifier on a given dataset
#  You can filter dataset by setting attributes, which you want to exclude
#
#  Usage: python crossvalidation.py "<attributes to exclude>"
#
######
import sys
import traceback
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier, Evaluation, PredictionOutput
from weka.core.classes import Random
from weka.filters import Filter

# filtered_attr may be: "1" or "first" - excludes first attribute from dataset ||
#                       "1-3" - excludes 1,2 and 3 attributes
#                       "4-8, 17, 19-20" - excludes 4,5,6,7,8,17,19,20 attributes
def cross_validate(dataset, folds_number, filtered_attr):
    # load ARFF data set
    loader = Loader(classname="weka.core.converters.ArffLoader")
    data = loader.load_file(dataset)
    data.class_is_last()

    # set KNN classifier
    classifier = Classifier(classname='weka.classifiers.lazy.IBk', options=["-K", "3"])
    
    # filter dataset
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", filtered_attr])
    remove.inputformat(data)
    filtered_data=remove.filter(data)
    
    # evaluate filtered data with n-fold-cross-validation; n = folds_number
    evaluation = Evaluation(filtered_data)
    evaluation.crossvalidate_model(classifier,filtered_data, folds_number, Random(65))
	
    # print statistic
    print(evaluation.summary())  

try:
    jvm.start()
    cross_validate("housingdata_train.arff", 5, sys.argv[1])
except Exception, e:
    print(traceback.format_exc())
finally:
    jvm.stop()
