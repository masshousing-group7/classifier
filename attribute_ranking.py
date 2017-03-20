#!/usr/bin/env python

##############################################################################
# Perform attribute ranking on the data set
##############################################################################

import traceback
import weka.core.jvm as jvm
from weka.filters import Filter
from weka.core.converters import Loader
from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection


######
# rank attributes from data having highest correlation with
# successful prediction
#
# takes data set loaded from file
# returns list of attribute indices with highest correlation
######
def rank_attributes(data_set):
  selector = AttributeSelection()
  evaluator = ASEvaluation(classname='weka.attributeSelection.CfsSubsetEval',\
                                                      options = ['-P 4 -E 4'])
  searcher = ASSearch(classname='weka.attributeSelection.GreedyStepwise',\
                                                             options=['-R'])
  selector.jwrapper.setEvaluator(evaluator.jobject)
  selector.jwrapper.setSearch(searcher.jobject)
  selector.select_attributes(data_set)
  return selector.selected_attributes.tolist()


##############################################################################
# if this script is executed directly, run the selector and print the
# selected indices
##############################################################################

if __name__ == '__main__':

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

    print rank_attributes(filtered_data)
  except Exception, e:
    print(traceback.format_exc())
  finally:
    jvm.stop()
