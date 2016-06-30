import random

child = []
with open('child_diff_log.txt') as it:
	for line in it:
		child.append(line.strip())

random.shuffle(child)

neg = []
with open('negative.txt') as it:
	for line in it:
		neg.append(line.strip())

random.shuffle(neg)

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
