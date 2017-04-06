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
def cross_validate(data, folds_number, filtered_attr, classifier):
    # load ARFF data set
    # loader = Loader(classname="weka.core.converters.ArffLoader")
    # data = loader.load_file(dataset)
    # data.class_is_last() 
    
    # filter dataset
    filter = Filter(classname='weka.filters.unsupervised.attribute.RemoveType',\
                                                       options=['-T', 'string'])
    
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove",\
                                      options=['-V', '-R', filtered_attr]) 
    multi = MultiFilter()
    multi.filters = [remove, filter]
    #multi.filters = [filter]
    multi.inputformat(data)
    filtered_data=multi.filter(data)
    
    # evaluate filtered data with n-fold-cross-validation; n = folds_number
    evaluation = Evaluation(filtered_data)
    evaluation.crossvalidate_model(classifier,filtered_data, folds_number, Random(65))
	
    # print statistic
    print(evaluation.summary())
    print(evaluation.class_details())
    print(evaluation.matrix())	
   
if __name__ == '__main__':
  try:
      jvm.start()
    # load ARFF data set
      loader = Loader(classname='weka.core.converters.ArffLoader')
      data = loader.load_file('housingdata_train.arff')
      data.class_is_last()

      remove = Filter(classname='weka.filters.unsupervised.attribute.Remove',\
                                           options=['-R', '111,112'])
      remove.inputformat(data)
      no_strings = remove.filter(data)
      n = 81 # keep the top n features
      features = rank_attributes(no_strings)
      features = features[0:n]
      features = map(lambda e: e + 1, features) # index offset by 1
      features.extend([113])
      feature_string = ','.join(map(str, features))
	  
      clf = Classifier(classname="weka.classifiers.trees.J48")
      classifier = Classifier(classname="weka.classifiers.meta.MultiClassClassifier")
      classifier.options=["-M","2","-W", "weka.classifiers.trees.J48","--", "-C","0.25","-B"]
      print(classifier.options)
      
      cross_validate(data, 5, feature_string, classifier)
  except Exception, e:
      print(traceback.format_exc())
  finally:
      jvm.stop()
