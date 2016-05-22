# the functions in this file will be called in clr.py to calculate clr.

import math
import numpy as np

def SplineKnots(u, n, t):
	d = n - 1
	for j in xrange(0, d + t):
		if j < t:
			u[j] = 0
		elif j <= d:
			u[j] = u[j - 1] + 1
		else:
			u[j] = u[d] + 1
	return u

def max(data, numSamples):
	curMax = data[0]
	for curSample in xrange(1, numSamples):
		if data[curSample] > curMax:
			curMax = data[curSample]
	return curMax

def min(data, numSamples):
	curMin = data[0]
	for curSample in xrange(1, numSamples):
		if data[curSample] < curMin:
			curMin = data[curSample]
	return curMin

def xToZ(fromData, toData, numSamples, splineOrder, numBins):
	xMax = max(fromData, numSamples)
	xMin = min(fromData, numSamples)
	for curSample in xrange(0, numSamples):
		if xMax == xMin:
			toData.append(np.nan)
		else:
			toData.append((fromData[curSample] - xMin) * 
			(numBins - splineOrder + 1) / float(xMax - xMin))
	return toData

def SplineBlend(k, t, u, v, n):
	value = 0.0
	if t == 1:
		if ((u[k] <= v) and (v < u[k + 1])) or ((abs(v - u[k + 1]) < 1e-10) and (k + 1 == n)):
			value = 1
		else:
			value = 0
	else:
		d1 = u[k + t - 1] - u[k]
		d2 = u[k + t] - u[k + 1]
		if (d1 == 0) and (d2 == 0):
			value = 0
		elif d1 == 0:
			value = (u[k + t] - v) / float(d2) * SplineBlend(k + 1, t - 1, u, v, n)
		elif d2 == 0:
			value = (v - u[k]) / float(d1) * SplineBlend(k, t - 1, u, v, n)
		else:
			value = (v - u[k]) / float(d1) * SplineBlend(k, t - 1, u, v, n) + (u[k + t] - v) / float(d2) * SplineBlend(k + 1, t - 1, u, v, n)
		if value < 0:
			value = 0
	return value

def findWeights(x, knots, weights, numSamples, splineOrder, numBins):
	z = []
	xToZ(x, z, numSamples, splineOrder, numBins)
	for curSample in xrange(0, numSamples):
		for curBin in xrange(0, numBins):
			weights[curBin * numSamples + curSample] = SplineBlend(curBin, splineOrder, knots, z[curSample], numBins)
	return weights

def hist1d(x, knots, hist, w, numSamples, splineOrder, numBins):
	for curBin in xrange(0, numBins):
		for curSample in xrange(0, numSamples):
			hist[curBin] += w[curBin * numSamples + curSample] / float(numSamples)

def log2d(x):
	return math.log(x) / math.log(2)

def entropy1d(x, knots, weights, numSamples, splineOrder, numBins):
	hist = np.zeros(numBins)
	H = 0
	hist1d(x, knots, hist, weights, numSamples, splineOrder, numBins)
	for curBin in xrange(0, numBins):
		if hist[curBin] > 0:
			H -= hist[curBin] * log2d(hist[curBin])
	return H

def hist2d(x, y, knots, wx, wy, hist, numSamples, splineOrder, numBins):
	sum = 0.0;
	for curBinX in xrange(0, numBins):
		for curBinY in xrange(0, numBins):
			for curSample in xrange(0, numSamples):
				hist[curBinX * numBins + curBinY] += wx[curBinX * numSamples + curSample] * wy[curBinY * numSamples + curSample] / numSamples

def entropy2d(x, y, knots, wx, wy, numSamples, splineOrder, numBins):
	hist = []
	for i in range(numBins * numBins):
		hist.append(0.0)
	H = 0.0
	incr = 0.0
	hist2d(x, y, knots, wx, wy, hist, numSamples, splineOrder, numBins)
	for curBinX in xrange(0, numBins):
		for curBinY in xrange(0, numBins):
			incr = hist[curBinX * numBins + curBinY]
			if incr > 0:
				H -= incr * log2d(incr)
	return H

def calcSplineMI(x, y, numSamples, splineOrder, numBins):
	numBins = 2 if numBins < 2 else numBins
	numBins = 15 if numBins > 15 else numBins
	entropy1 = 0.0
	entropy2 = 0.0
	res = 0.0
	knots = range(numBins + splineOrder)
	knots[numBins + splineOrder - 1] = 0
	weightsX = range(numBins * numSamples)
	weightsY = range(numBins * numSamples)
	SplineKnots(knots, numBins, splineOrder)
	findWeights(x, knots, weightsX, numSamples, splineOrder, numBins)
	findWeights(y, knots, weightsY, numSamples, splineOrder, numBins)
	entropy1 = entropy1d(x, knots, weightsX, numSamples, splineOrder, numBins)
	entropy2 = entropy1d(y, knots, weightsY, numSamples, splineOrder, numBins)
	res = float(entropy1) + float(entropy2) - float(entropy2d(x, y, knots, weightsX, weightsY, numSamples, splineOrder, numBins))
	return res

def calcDTI(x, y, rowNum, colNum):
	numBins = 6
	splineOrder = 3
	newY = range(rowNum * (colNum + 1))
	for i in xrange(0, rowNum):
		newY[i] = 0
	for j in xrange(0, len(y)):
		newY[i + 1] = y[j]
		i += 1
	dti = calcSplineMI(x, y, rowNum, splineOrder, numBins)
	for j in xrange(2, colNum + 1):
		dti += calcSplineMI(x, y, rowNum * j, splineOrder, numBins) - calcSplineMI(x, newY, rowNum * j, splineOrder, numBins)
	return dti
