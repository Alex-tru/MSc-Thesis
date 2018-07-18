#!/usr/bin/python

import validation
import numpy as np

"Run validation script for all results files of an experiment, comparing against one of them."




## convergence measure limit

max_exp = 8
N_experiments = 8
varied_values = np.concatenate([ 1./10.**np.arange(1, max_exp+1, N_experiments/max_exp), 1e-2 * np.arange(2,10) ])


pathA1 = "conv_limit_1e-08_beam1.dat"
pathA2 = "conv_limit_1e-08_beam2.dat"

for value in varied_values:
	pathB1 = "conv_limit_" + '{0:.0e}'.format(value) + "_beam1.dat"
	pathB2 = "conv_limit_" + '{0:.0e}'.format(value) + "_beam2.dat"
	validation.part_vs_part( pathA1, pathA2, pathB1, pathB2 )
