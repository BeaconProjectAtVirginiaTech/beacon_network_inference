#!/usr/bin/python
# -*- coding: utf-8 -*-
# compute clrs for all gene pairs, the output are clr values.

import sys
import os
import argparse
import numpy as np
import math
from functions import calcDTI

def parse_args():
    """
    Parse the parameters
    """
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=str, 
            help="the gene expression file without gene name")
    ap.add_argument('--output', type=str, 
            default="./step1_result.csv",
            help="the result file")
    return ap.parse_args()

#compute directed mutual information value for each of the gene pairs
def compute_dti(input_filename):
    args = parse_args()
    input_f = open(input_filename)
    exp_data = [map(float, line.strip().split('\t'))
            for line in input_f]
    input_f.close()
    n = len(exp_data)
    dti_matrix = np.zeros((n, n))
    for i, item_i in enumerate(exp_data):
        for j, item_j in enumerate(exp_data):
            dti_matrix[i, j] = calcDTI(item_i, item_j, 1, 7)
    return dti_matrix

def main():
    args = parse_args()
    #compute n * n dti matrix
    dti_matrix = compute_dti(args.input)
    num_gene = len(dti_matrix[0])
    rowVars = []
    colVars = []
    rowMeans = []
    colMeans = []
    score_matrix = np.zeros((num_gene, num_gene))
    for i in dti_matrix:
        rowMeans.append(np.mean(i))
        rowVars.append(np.std(i, ddof = 1))
    column = zip(*dti_matrix)
    for i in column:
        colMeans.append(np.mean(i))
        colVars.append(np.std(i, ddof = 1))
    #from dti matrix to compute clr score matrix
    for i in xrange(0, num_gene):
        for j in xrange(0, num_gene):
            score_matrix[i, j] = math.sqrt(math.pow(((dti_matrix[i, j] - rowMeans[i]) / rowVars[i]), 2) + math.pow(((dti_matrix[i, j] - colMeans[j]) / colVars[j]), 2))
    np.savetxt(args.output, score_matrix, delimiter='\t', fmt="%0.5f")
    return score_matrix

if __name__ == "__main__":
    main()
