#!/usr/bin/env python

"""Train a document classifier."""

import reuters
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
import time
from sklearn.svm import LinearSVC


def main(dataset_module):
    """
    Train a classifier for a dataset.

    Parameters
    ----------
    categories : list of str
    document_ids : list of str
    """
    # Calculate feature vectors
    data = dataset_module.load_data()

    xs = {'train': data['x_train'], 'test': data['x_test']}
    ys = {'train': data['y_train'], 'test': data['y_test']}

    # Get classifiers
    classifiers = [
        ('Decision Tree', DecisionTreeClassifier(max_depth=5)),
        ('LinearSVC', OneVsRestClassifier(LinearSVC(random_state=42))),
        ('Random Forest (50 estimators)',
         RandomForestClassifier(n_estimators=50, n_jobs=10)),
        ('Random Forest (200 estimators)',
         RandomForestClassifier(n_estimators=200, n_jobs=10)),
        ('Logistic Regression (C=1)',
         OneVsRestClassifier(LogisticRegression(C=1))),
        ('Logistic Regression (C=1000)',
         OneVsRestClassifier(LogisticRegression(C=10000))),
        ('Naive Bayes', OneVsRestClassifier(GaussianNB())),
        ('SVM, linear', OneVsRestClassifier(SVC(kernel="linear",
                                                C=0.025,
                                                cache_size=200))),
        ('SVM, adj.', OneVsRestClassifier(SVC(probability=False,
                                              kernel="rbf",
                                              C=2.8,
                                              gamma=.0073,
                                              cache_size=200))),
        ('k nn 3', KNeighborsClassifier(3)),
        ('k nn 5', KNeighborsClassifier(5)),
        ('AdaBoost', OneVsRestClassifier(AdaBoostClassifier())),  # 20 minutes to train
        ('LDA', OneVsRestClassifier(LinearDiscriminantAnalysis())),  # took more than 6 hours
        ('RBM 100', Pipeline(steps=[('rbm', BernoulliRBM(n_components=100)),
                                    ('logistic', LogisticRegression(C=1))])),
        # ('RBM 100, n_iter=20',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=100, n_iter=20)),
        #                  ('logistic', LogisticRegression(C=1))])),
        # ('RBM 256', Pipeline(steps=[('rbm', BernoulliRBM(n_components=256)),
        #                             ('logistic', LogisticRegression(C=1))])),
        # ('RBM 512, n_iter=100',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=512, n_iter=10)),
        #                  ('logistic', LogisticRegression(C=1))])),
    ]

    for clf_name, classifier in classifiers:
        t0 = time.time()
        classifier.fit(xs['train'], ys['train'])
        t1 = time.time()
        score = classifier.score(xs['test'], ys['test'])
        t2 = time.time()
        print(("{clf_name:<30}: {score:0.2f}% in {train_time:0.2f}s train / "
               "{test_time:0.2f}s test")
              .format(clf_name=clf_name,
                      score=(score * 100),
                      train_time=t1 - t0,
                      test_time=t2 - t1))

if __name__ == '__main__':
    main(reuters)