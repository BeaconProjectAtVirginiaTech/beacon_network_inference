#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is to infer new connections

import sys
import os
import argparse
from sklearn.svm import LinearSVC
import numpy as np
import json
from sklearn import svm

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trainFile", type=str,
        help="training examples")
    ap.add_argument("--testFile", type=str,
        help="the gene pair labels to be inferred")
    return ap.parse_args()

def classify(trainFile, testFile):
    xTrain = []
    yTrain = []
    xTest = []
    testLines = []

    with open(trainFile) as trainF, open(testFile) as testF:
        d_len = 0
        # xTrain is the feature values of the training examples
        # yTrain is the labels of the training examples
        for line in trainF:
            info = line.strip().split('\t')
            temp = []
            for i in info[1:]:
                temp.append(float(i))
            xTrain.append(temp)

        ix = 0
        # xTest is the feature values of the inferred gene pairs
        for line in testF:
            info = line.strip().split('\t')
            temp = []
            for i in info[1:]:
                temp.append(float(i))
            xTest.append(temp)
            testLines.append(line)
            ix += 1

    xTrain = np.array(xTrain)
    xTest = np.array(xTest)
    yTrain = np.array(yTrain)

    print xTrain.shape, xTest.shape, yTrain.shape

    #this is to call rbf svm.
    clf = svm.SVC(C=1000,probability = True,gamma=1/128)
    clf.fit(xTrain, yTrain)
    preds = clf.predict(xTest)
    #output confidence of the prediction
    probs = clf.predict_proba(xTest)

    resultFile = "./res.txt"
    #write output file. The first several columns are the same as the inference
    #file, the additional last two columns are label of the gene pair and the
    #confidence score.
    with open(resultFile, 'w') as rf:
        for i, line in enumerate(testLines):
            p = preds[i]
            prob = probs
            rf.write("%s\t%f\t%d\n" % (line.strip(), float(probs[i][1]), int(p)))
def main():
    args = parse_args()
    trainFile = args.trainFile
    testFile = args.testFile

    classify(trainFile, testFile)
    

if __name__ == "__main__":
    main()

