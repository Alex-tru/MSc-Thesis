#!/usr/bin/python

import validation
import numpy as np

"Run validation script for all results files of an experiment."




## convergence measure limit

min_exp = 2 
N_experiments = 6
varied_values1 = 1./10.**np.arange( min_exp, min_exp + N_experiments )
varied_values2 = 1e-2 * np.arange(2,6)
varied_values = np.concatenate([ varied_values1, varied_values2 ])

path_mono = "reference/beam_mono.dat"

for value in varied_values:
	path1 = "conv_limit_" + '{0:.0e}'.format(value) + "_beam1.dat"
	path2 = "conv_limit_" + '{0:.0e}'.format(value) + "_beam2.dat"
	validation.validate( path1, path2, path_mono )
