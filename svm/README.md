This folder contains two folders.

evaluate: evaluation of the svm performance by 3 fold cross validation and ROC curves
infer: classify unknown gene pairs with prediction confidence.


Gene expression data and prior known interactions and non-interactions are required as the input.

The features of used in here are log-2 fold change of the expression of target over the expression of the regulator at one time point before. So before runnining the algorithm, the expression data should be converted to this log-2 fold change.