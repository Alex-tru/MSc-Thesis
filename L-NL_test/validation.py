#!/usr/bin/python

"""
Validate results of partitioned against monolithic simulation of the beam test case.
"""

import math

import argparse

parser = argparse.ArgumentParser()
parser.add_argument( "beam1" )
parser.add_argument( "beam2" )
parser.add_argument( "mono" )
args = parser.parse_args()

############################# params #################################

# size of complete node sets
#nsize1 = 201
#nsize2 = 81
#nsizem = 261 # nsize1 + nsize2 - nsurface_size
#nsize1 = 2225
#nsize2 = 785
#nsizem = 2945 # nsize1 + nsize2 - nsurface_size
#nsize1 = 14913
#nsize2 = 5121
#nsizem = 19809
nsize1 = 4320
nsize2 = 1488
nsizem = 5736

#surf = [ 783, 784, 785, 786, 791, 792, 793, 794, 795, 796, 799, 800, 801, 802, 803, 806, 807, 808, 809, 810, 813, 814, 815, 1531, 1532, 1535, 1536, 1537, 1538, 1540, 1541, 1542, 1544, 1545, 1546, 1548, 1549, 2153, 2154, 2157, 2158, 2159, 2160, 2162, 2163, 2164, 2166, 2167, 2168, 2170, 2171, 2775, 2776, 2779, 2780, 2781, 2782, 2784, 2785, 2786, 2788, 2789, 2790, 792, 2793 ]

#surf = [ 2911, 2912, 2913, 2914, 2919, 2920, 2921, 2922, 2923, 2924, 2927, 2928, 2929, 2930, 2931, 2934, 2935, 2936, 2937, 2938, 2941, 2942, 2943, 2944, 2945, 2948, 2949, 2950, 2951, 2952, 2955, 2956, 2957, 2958, 2959, 2962, 2963, 2964, 2965, 2966, 2969, 2970, 2971, 5619, 5620, 5623, 5624, 5625, 5626, 5628, 5629, 5630, 5632, 5633, 5634, 5636, 5637, 5638, 5640, 5641, 5642, 5644, 5645, 5646, 5648, 5649, 5650, 5652, 5653, 7885, 7886, 7889, 7890, 7891, 7892, 7894, 7895, 7896, 7898, 7899, 7900, 7902, 7903, 7904, 7906, 7907, 7908, 7910, 7911, 7912, 7914, 7915, 7916, 7918, 7919, 10151, 10152, 10155, 10156, 10157, 10158, 10160, 10161, 10162, 10164, 10165, 10166, 10168, 10169, 10170, 10172, 10173, 10174, 10176, 10177, 10178, 10180, 10181, 10182, 10184, 10185, 12417, 12418, 12421, 12422, 12423, 12424, 12426, 12427, 12428, 12430, 12431, 12432, 12434, 12435, 12436, 12438, 12439, 12440, 12442, 12443, 12444, 12446, 12447, 12448, 12450, 12451, 14683, 14684, 14687, 14688, 14689, 14690, 14692, 14693, 14694, 14696, 14697, 14698, 14700, 14701, 14702, 14704, 14705, 14706, 14708, 14709, 14710, 14712, 14713, 14714, 14716, 14717, 16949, 16950, 16953, 16954, 16955, 16956, 16958, 16959, 16960, 16962, 16963, 16964, 16966, 16967, 16968, 16970, 16971, 16972, 16974, 16975, 16976, 16978, 16979, 16980, 16982, 16983, 19215, 19216, 19219, 19220, 19221, 19222, 19224, 19225, 19226, 19228, 19229, 19230, 19232, 19233, 19234, 19236, 19237, 19238, 19240, 19241, 19242, 19244, 19245, 19246, 19248, 19249 ]

surf = [ 2744, 2747, 2748, 2751, 2752, 2755, 2756, 2759, 2760, 2763, 2764, 2767, 
2768, 2771, 2772, 2775, 2776, 3010, 3011, 3014, 3015, 3018, 3019, 3022, 
3023, 3026, 3027, 3030, 3031, 3034, 3035, 3038, 3039, 3266, 3267, 3270, 
3271, 3274, 3275, 3278, 3279, 3282, 3283, 3286, 3287, 3290, 3291, 3294, 
3295, 3515, 3516, 3519, 3520, 3523, 3524, 3527, 3528, 3531, 3532, 3535, 
3536, 3539, 3540, 3543, 4520, 4521, 4554, 4555, 4588, 4589, 4622, 4623]

surf_indx = [x-1 for x in surf]# -1 because node indices start at 1

step_length = 1e-7

# tolerance for comparing values
tol = 1e-06

##################################################################

def read_dat( dat_path, nsize, first_node, last_node, comp_step ):
	"""
	Reads values in .dat results file and returns a dictionary with them.
	"""
	with open(dat_path) as f:
		# keys of beam dict are timesteps. values are nested lists
		# for each node such as: [[# of node, Dx, Dy, Dz], ...]
		beam = {}	
	
		while(True):
			f.readline()
			step_header = f.readline()
			if not(step_header): break
			step = float(step_header.split("time  ")[-1])

			#these 3 lines are used when no. of steps is too large to keep all steps
			if abs( step - comp_step ) > 1e-15: 
				#skipping the step without storing
				for i in xrange(nsize+1): f.readline()
				continue

			data_type = step_header.strip()[0]
			# initialize list only when reading displacements (first dataset of the node)
			if data_type == "d":
				# (3 displacements + 3 forces) * nsizem nodes
				beam[step] = [[0.,0.,0.,0.,0.,0.]] * nsizem			
			f.readline()			
			# iterate over nodes
			if data_type == "d":
				for i in xrange(nsize):
					# parse and store node number and displacements
					line = f.readline().strip().split(" ")
					beam[step][int(line[0])-1] = [float(x) for x in line[1:] if x]
			else:
				for i in xrange(nsize):
					# parse and store node number and forces
					line = f.readline().strip().split(" ")
					beam[step][int(line[0])-1] += [float(x) for x in line[1:] if x]
#		print beam.keys()
	return beam

def compare_beam_step( beam1, beam2, beam_mono, tol ):
	"""
	Compares displacements & forces, in all nodes, between the beam1_beam2 union and beam_mono. Computes L2 norms of the error.
    Returns true if values are equal.
	"""

	## merge beams
	beam_part = [[x+y for x,y in zip(beam1[i],beam2[i])] for i in xrange(nsizem)]
	# on the surface, compute average
	for i in surf_indx:
		beam_part[i] = [(x+y)/2. for x,y in zip(beam1[i],beam2[i])]

	error = [[abs(xi - yi) for xi,yi in zip(x,y)] for x,y in zip(beam_part,beam_mono)]
	if any([any([xi > tol for xi in x]) for x in error]):
		print "Validation unsuccessful!"
	else: print "Validation successful!"
#		print [[xi  for xi in x] for x in error]

	## relative error
	rel_err = [[xi/(abs(yi+1e-30)) for xi,yi in zip(x,y)] for x,y in zip(error,beam_mono)]

	## L2_norm

	# global: (L2 norm of the L2 norms of each node's error)
	L2d = math.sqrt(sum([math.sqrt(sum([x*x for x in error[i][:3]])) for i in xrange(nsizem)]))
	L2f = math.sqrt(sum([math.sqrt(sum([x*x for x in error[i][3:]])) for i in xrange(nsizem)])) 

	# component-wise: (L2 norm of the vector containing one component of each node's error)
	L2dx = math.sqrt(sum([error[i][0]**2 for i in xrange(nsizem)]))
	L2dy = math.sqrt(sum([error[i][1]**2 for i in xrange(nsizem)]))
	L2dz = math.sqrt(sum([error[i][2]**2 for i in xrange(nsizem)]))
	L2fx = math.sqrt(sum([error[i][3]**2 for i in xrange(nsizem)]))
	L2fy = math.sqrt(sum([error[i][4]**2 for i in xrange(nsizem)]))
	L2fz = math.sqrt(sum([error[i][5]**2 for i in xrange(nsizem)]))


	## output
#	print "Displacement errors:"
#	for i in xrange(nsizem):
#		print "Node", i+1, [": %.4e" % x for x in error[i][:3]]
#	print "Relative errors (error/ref.displacement) (using beam_mono displacements as ref.):"
#	for i in xrange(nsizem):
#		print "Node", i+1, [" %.2f" % x for x in rel_err[i][:3]]	

#	print "Force errors"
#	for i in xrange(nsizem):
#		print "Node", i+1, [": %.4e" % x for x in error[i][3:]]
#	print "Relative errors (error/ref.force) (using beam_mono  as ref.):"
#	for i in xrange(nsizem):
#		print "Node", i+1, [" %.2f" % x for x in rel_err[i][3:]]	
	print "Global L2 norm of displacement error =", L2d
#	print "L2 norm of component x of displacement error=", L2dx
#	print "L2 norm of component y of displacement error=", L2dy
#	print "L2 norm of component z of displacement error =", L2dz	
#	print "Global L2 norm of force error =", L2f
#	print "L2 norm of component x of force error=", L2fx
#	print "L2 norm of component y of force error=", L2fy
#	print "L2 norm of component z of force error =", L2fz		

	return [L2d, L2dx, L2dy, L2dz, L2f, L2fx, L2fy, L2fz]

###############################################################################
################################# MAIN ##############################################




with open( "dt_1e-7_L-NL_split-errorVStime.csv", "w" ) as fw:

	fw.write( "t, L2d, L2dx, L2dy, L2dz, L2f, L2fx, L2fy, L2fz\n" )

	for step_no in range( 100, 10001, 100 ):

		comp_step = round( step_no * step_length, 6 )

		#beam1 = read_dat( args.beam1, nsize1, 1, 2793 )
		beam1 = read_dat( args.beam1, nsize1, 1, 19249, comp_step)
		#beam2 = read_dat( args.beam2, nsize2, 783, nsizem )
		beam2 = read_dat( args.beam2, nsize2, 2911, nsizem, comp_step )
		beam_mono = read_dat( args.mono, nsizem, 1, nsizem, comp_step )

		L2_errors = compare_beam_step( beam1[comp_step], beam2[comp_step], beam_mono[comp_step], tol )
		fw.write( ", ".join( [ str(x) for x in [comp_step] + L2_errors ] ) + "\n" )

#with open()
#print "----------------BEAM 1 at t=0.5----------------------------"
#print beam1[0.5]
#print "----------------BEAM 2 at t=0.5----------------------------"
#print beam2[0.5]
#print "----------------BEAM MONO at t=0.5-------------------------"
#print beam_mono[0.5]

