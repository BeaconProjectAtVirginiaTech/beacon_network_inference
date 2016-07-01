The test is done on three regulators separately: ABI3, FUS3 and LEC1.

In each folder, there are XXXX_positive.txt and XXXX_negative.txt files and these files have known interactions and non-interactions.

3fold.py randomly splits the positive and negative examples into 3 parts. 
Run 3fold.py: python 3fold.py --positive XXXX_positive.txt --negative XXXX.negative.txt
The output of this command are 3 positive example files XXXX_pos_1 through XXXX_pos_3.txt, and 3 negative example files XXXX_neg_1 through XXXX_neg_3.txt
The evaluation is done by training 2 of the positive and negative sets and testing on the last subset. For example, to train on the first two subsets and test on the last subset, you need to combine XXXX_pos_1 and XXXX_pos_2 to get XXXX_pos.txt, and combine XXXX_neg_1 and XXXX_neg_3 to get XXXX_neg.txt.
Run evaluation.py: python evaluation.py --trainFile XXXX_pos.txt --testFile XXXX_neg.txt
The output of this command is an ROC curve that shows the performance of the algorithm and and AUC value. These can be used to evaluate and compare the method.