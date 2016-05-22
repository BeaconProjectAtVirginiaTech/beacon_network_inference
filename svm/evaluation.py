'''
This file is the evaluation of svm. The input files are training and testing gene
pairs. In the evaluation, all the gene pairs have known labels. The input files are
in the following format: gene pair ids in the first two columns, the feature values 
are in the following columns, and the last column is the label of the gene pair.
'''
import json
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.multiclass import OneVsRestClassifier
from sklearn import svm, datasets
import numpy as np
from sklearn.svm import LinearSVC

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trainFile", type=str,
    	help="training examples with expression profiles")
    ap.add_argument("--testFile", type=str,
    	help="unknown gene pairs to classify")
    return ap.parse_args()

def main():
	args = parse_args()
	x_train = []
	x_test = []
	y_train = []
	y_test = []
	y_score = []

	'''x_train is feature vectors of training examples. LOCAL MODEL: log-2 fold 
	change of the expression value target over the expression value of regulator 
	at one time point before. GLOBAL MODEL: concatenation of expression profiles
	of regulator and target. 
	y_train is the label of each training example.
	'''
	with open(args.trainFile) as it:
		for line in it:
			info = line.strip().split('\t')
			temp = []
			for i in info[1:-1]:
				temp.append(float(i))
			y_train.append(int(info[-1]))
			x_train.append(temp)
	#x_test is the feture vector list of testing gene pairs. 
	#y_test is the label of each testing gene pair.
	with open(args.testFile) as it:
		for line in it:
			info = line.strip().split('\t')
			temp = []
			for i in info[1:-1]:
				temp.append(float(i))
			y_test.append(int(info[-1]))
			x_test.append(temp)

	# this is the svm with rbf kernel
	clf = svm.SVC(C=1000, probability=True, gamma=1/128)
	#this is the svm with linear kernel
	#clf = svm.SVC(C=1000, probability=True)

	y_score = clf.fit(x_train, y_train).decision_function(x_test)

	fpr, tpr, t = roc_curve(y_test, y_score)

	#generate roc curves
	roc_auc = auc(fpr, tpr)
	plt.figure()
	plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
	plt.plot([0, 1], [0, 1], 'k--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver operating characteristic example')
	plt.legend(loc="lower right")
	plt.show()

if __name__ == "__main__":
    main()