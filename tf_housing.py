from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from sklearn import datasets
from sklearn import metrics
from sklearn import model_selection

import tensorflow as tf
import numpy as np


def main(unused_argv):
  # Load dataset.
  data = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename='housingdata_train.csv',
    target_dtype=np.int,
    features_dtype=np.float32)

  # split dataset into train and test datasets with 33% ratio
  x_train, x_test, y_train, y_test = model_selection.train_test_split(
      data.data, data.target, test_size=0.33, random_state=65)

  # Build 3 layer DNN with 10, 20, 10 units respectively.
  feature_columns = tf.contrib.learn.infer_real_valued_columns_from_input(
      x_train)
  classifier = tf.contrib.learn.DNNClassifier(
      feature_columns=feature_columns, 
      activation_fn = tf.nn.softplus, 
      hidden_units=[10, 20, 30, 20, 10], 
      n_classes=5,
      #optimizer=tf.train.ProximalAdagradOptimizer(
      #               learning_rate=0.1,
      #               l1_regularization_strength=0.001)
   )

  # Fit and predict.
  classifier.fit(x_train, y_train, steps=200)
  predictions = list(classifier.predict(x_test, as_iterable=True))
  score = metrics.accuracy_score(y_test, predictions)
  print('Accuracy: {0:f}'.format(score))


if __name__ == '__main__':
  tf.app.run()
