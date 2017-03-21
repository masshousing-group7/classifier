######
#
#  Script performs 5 - fold - cross - validation for KNN classifier on a given dataset
#  You can filter dataset by setting attributes, which you want to exclude
#
#  Usage: python crossvalidation.py 
#
######
import sys
import traceback
import itertools
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier, Evaluation, PredictionOutput
from weka.core.classes import Random
from weka.filters import Filter, MultiFilter
from attribute_ranking import rank_attributes

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
    filter = Filter(classname='weka.filters.unsupervised.attribute.RemoveType',\
                                                       options=['-T', 'string'])
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", filtered_attr])
    multi = MultiFilter()
    multi.filters = [remove, filter]
    multi.inputformat(data)
    filtered_data=multi.filter(data)
    
    # evaluate filtered data with n-fold-cross-validation; n = folds_number
    evaluation = Evaluation(filtered_data)
    evaluation.crossvalidate_model(classifier,filtered_data, folds_number, Random(65))
	
    # print statistic
    print str(evaluation.summary())
   
try:
    jvm.start()
	    # load ARFF data set
    loader = Loader(classname='weka.core.converters.ArffLoader')
    data = loader.load_file('housingdata_train.arff')
    data.class_is_last()

    # filter string values
    filter = Filter(classname='weka.filters.unsupervised.attribute.RemoveType',\
                                                       options=['-T', 'string'])
    filter.inputformat(data)
    filtered_data = filter.filter(data)
	
    list = list(rank_attributes(filtered_data))
    list = list[-26:]
   # for i in xrange(2, 26):
   # for index, inst in enumerate(itertools.combinations(list, 25)):
       # attr= ', '.join(map(str, inst))
    attr = "50, 53, 68, 41, 45, 31, 34, 40, 44, 60, 61, 63, 67, 70, 72"
    cross_validate("housingdata_train.arff", 5, attr)
except Exception, e:
    print(traceback.format_exc())
finally:
    jvm.stop()
