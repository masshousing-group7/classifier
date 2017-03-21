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

# function to translate the grade
def get_grade(grade):
    if (grade == 1.0):
        return "GOOD"
    else:
        return "BAD"

def main():

    # load a dataset
    loader = Loader("weka.core.converters.ArffLoader")
    data = loader.load_file("housingdata_train.arff")
    data.class_is_last()

    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "73,74, 50, 53, 68, 41, 45, 31, 34, 40, 44, 60, 61, 63, 67, 70, 72"]) 
    # classifier
    classifier = Classifier(classname='weka.classifiers.lazy.IBk', options=["-K", "3"])
    fc = FilteredClassifier()
    fc.filter = remove
    fc.classifier = classifier

    # randomize data
    folds = 5
    seed = 1
    rnd = Random(seed)
    rand_data = Instances.copy_instances(data)
    rand_data.randomize(rnd)
    if rand_data.class_attribute.is_nominal:
        rand_data.stratify(folds)
    
    f = open("cross_validation_output.txt", "w")
    # perform cross-validation 
    evaluation = Evaluation(rand_data)
    for i in xrange(folds):
        train = rand_data.train_cv(folds, i)
        test = rand_data.test_cv(folds, i)

        # build and evaluate classifier
        cls = Classifier.make_copy(fc)
		
        cls.build_classifier(train)
        evaluation.test_model(cls, test)

         # create a filtered classifier
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
                f.write(" Rm_key: " + str(inst.get_string_value(72)) +  
                        " Stmt_date: " + str(inst.get_string_value(73)) +
                        " expected grade: " + get_grade(inst.get_value(inst.class_index)) +
                        " predicted grade: " + get_grade(prediction) +
                        " class distribution: " + str(dist)+'\n')
        
    print(evaluation.summary("=== " + str(folds) + " -fold Cross-Validation ==="))

try:
    jvm.start()
    main()
except Exception, e:
    print(traceback.format_exc())
finally:
    jvm.stop()
