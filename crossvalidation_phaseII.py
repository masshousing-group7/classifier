##########
#
#   Custom 5-fold-cross-validation
#
#   Usage: python crossvalidation_custom.py
#
#########
import os
import traceback
import weka.core.jvm as jvm
from weka.core.classes import Random
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.classifiers import Classifier, Evaluation,  FilteredClassifier
from weka.filters import Filter, MultiFilter
from attribute_ranking import rank_attributes

# function to translate the grade
def get_grade(grade):
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

def main():

    # load a dataset
    loader = Loader("weka.core.converters.ArffLoader")
    data = loader.load_file("housingdata_train.arff")
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
    feature_string = feature_string.replace(',51','').replace(',49','').replace(',36','').replace(',44','').replace(',47','').replace(',48','').replace(',8,',',').replace(',10,',',')
    feature_string = feature_string.replace(',11,',',').replace(',13','').replace(',69','').replace(',42','').replace(',34','').replace(',72','').replace(',108','').replace(',60','')
    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove",\
                                      options=['-V', '-R', feature_string]) 
    clf = Classifier(classname="weka.classifiers.trees.J48")
    classifier = Classifier(classname="weka.classifiers.meta.MultiClassClassifier")
    classifier.options=["-M","2","-W", "weka.classifiers.trees.J48","--", "-C","0.25","-B"]
    
    fc = FilteredClassifier()
    fc.filter = remove
    fc.classifier = classifier

    # randomize data
    folds = 5
    seed = 65
    rnd = Random(seed)
    rand_data = Instances.copy_instances(data)
    rand_data.randomize(rnd)
    if rand_data.class_attribute.is_nominal:
        rand_data.stratify(folds)
    
    f = open("cross_validation_phaseII_output.txt", "w")
    # perform cross-validation 
    evaluation = Evaluation(rand_data)
    for i in xrange(folds):
        train = rand_data.train_cv(folds, i)
        test = rand_data.test_cv(folds, i)

        # build and evaluate classifier
        cls = Classifier.make_copy(fc)
		
        cls.build_classifier(train)
        evaluation.test_model(cls, test)

         # # create a filtered classifier
        fc = FilteredClassifier()
        fc.filter = remove
        fc.classifier = classifier
        fc.build_classifier(train)
        f.write("------ " + str(i+1) + " fold-------\n")
        for index, inst in enumerate(test):
        # predict the grade
            prediction = fc.classify_instance(inst)
            dist = cls.distribution_for_instance(inst)
        
        #if a predicted value doesn't match an actual grade
            if (inst.get_value(inst.class_index) != prediction):
                f.write(" Rm_key: " + str(inst.get_string_value(110)) +  
                        " Stmt_date_year: " + str(inst.get_string_value(111)) +
                        " expected grade: " + get_grade(inst.get_value(inst.class_index)) +
                        " predicted grade: " + get_grade(prediction) +
                        " class distribution: " + str(dist)+'\n')
	
    print 'Feature indices kept:', feature_string					
    print(evaluation.summary("=== " + str(folds) + " -fold Cross-Validation ==="))
    print(evaluation.matrix())

try:
    jvm.start()
    main()
except Exception, e:
    print(traceback.format_exc())
finally:
    jvm.stop()
