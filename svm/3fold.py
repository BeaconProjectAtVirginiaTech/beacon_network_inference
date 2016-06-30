#This file randomly split the positive and negative examples into three parts to perform in 3-fold validation.

import random

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--positive", type=str,
    	help="positive examples")
    ap.add_argument("--negative", type=str,
    	help="negative examples")
    return ap.parse_args()
#positive examples are randomly put into child
child = []
with open('positive.txt') as it:
	for line in it:
		child.append(line.strip())

random.shuffle(child)
# negative examples are randomly put into neg
neg = []
with open('negative.txt') as it:
	for line in it:
		neg.append(line.strip())

random.shuffle(neg)
#Three positive example files are pos_1, pos_2 and pos_3. Three negative example files are neg_1, neg_2, and neg_3.
with open('pos_1.txt', 'w') as otf, open('pos_2.txt', 'w') as otf2, open('pos_3.txt', 'w') as otf3, open('neg_1.txt', 'w') as otf4, open('neg_2.txt', 'w') as otf5, open('neg_3.txt', 'w') as otf6:
	for i in child[:32]:
		otf.write("%s\n" % i)

	for i in neg[:33]:
		otf4.write("%s\n" % i)

	for i in child[32:63]:
		otf2.write("%s\n" % i)

	for i in neg[33:66]:
		otf5.write("%s\n" % i)

	for i in child[63:]:
		otf3.write("%s\n" % i)

	for i in neg[66:]:
		otf6.write("%s\n" % i)
