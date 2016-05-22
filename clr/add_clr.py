#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import argparse
import numpy as np

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gene', type=str, 
            help='gene name file, the order should be the same as expression file in step 1')
    ap.add_argument('--clr', type=str,
            help='clr matrix from step 1')
    return ap.parse_args()

def main():
    args = parse_args()
    gene_file = args.gene
    gene2id = {}
    gene_name = []
    with open(gene_file) as gf:
        for line in (gf):
            gene_name.append(line.strip())
    with open(gene_file) as gf:
        gene2id = {line.strip(): i for i, line in enumerate(gf)}
        print gene2id
    dti_matrix = np.genfromtxt(args.dti, delimiter='\t')
    num_gene = len(gene_name)
    outfile_genepair = "./genepair_clr.txt"
    with open(outfile_genepair, 'w') as otf:
        for i in xrange(0, num_gene):
            g1 = gene_name[i]
            for j in xrange(0, num_gene):
                g2 = gene_name[j]
                otf.write("%s\t%s\t%0.5f\n" % (g1, g2, dti_matrix[i, j]))



if __name__ == "__main__":
    main()
