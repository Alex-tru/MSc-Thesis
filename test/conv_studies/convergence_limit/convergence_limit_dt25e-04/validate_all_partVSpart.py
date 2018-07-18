#!/usr/bin/python

import validation
import numpy as np

"Run validation script for all results files of an experiment, comparing against one of them."




## convergence measure limit

min_exp = 2 
N_experiments = 4
varied_values1 = 1./10.**np.arange( min_exp, min_exp + N_experiments )
varied_values2 = 1e-2 * np.arange(2,6)
varied_values = np.concatenate([ varied_values1, varied_values2 ])


pathA1 = "conv_limit_1e-05_beam1.dat"
pathA2 = "conv_limit_1e-05_beam2.dat"

for value in varied_values:
	pathB1 = "conv_limit_" + '{0:.0e}'.format(value) + "_beam1.dat"
	pathB2 = "conv_limit_" + '{0:.0e}'.format(value) + "_beam2.dat"
	validation.part_vs_part( pathA1, pathA2, pathB1, pathB2 )
