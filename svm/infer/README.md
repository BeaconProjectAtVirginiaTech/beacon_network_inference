To infer new relationships, we need all the positive examples and negative examples.

Combine positive example file XXXX_positive.txt and negative example file XXXX_negative.txt to get training.txt as the training set, and a list of genes test.txt to infer.
To run infer.py: python infer.py --trainFile training.txt --testFile test.txt
The output is a file with all the genes provided in the test.txt file with the last column showing 1 or 0. 1 means this gene is a potential target and 0 means not.