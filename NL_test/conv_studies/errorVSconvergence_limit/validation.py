#!/usr/bin/python

"""
Validate results of partitioned against monolithic simulation of the beam test case.
"""

import math

############################# nodes #################################

nset1 = [range(1,5),range(9,21),range(33,45),range(51,75),range(78,90),range(93,98),range(103,127),range(132,156),range(161,185),range(190,214),range(219,255)]
nset1_indx = [x-1 for y in nset1 for x in y]# -1 because node indices start at 1

nset2 = [range(5,9),range(21,33),range(44,52),range(74,78),range(89,93),range(98,103),range(124,132),range(153,161),range(182,190),range(211,219),range(250,261)]
nset2_indx = [x-1 for y in nset2 for x in y]# -1 because node indices start at 1

nsetm = range(1,261)

#interface
nsurface = [44,51,74,89,124,125, 126,153,154,155,182,183,184,211,212,213,250,251,252,253,254]
nsurf_indx = [x-1 for x in nsurface]# -1 because node indices start at 1

############################# params #################################

# size of control node set for beam 1, beam 2 and beam mono. set in ccx input files (.inp)
#nctrl_sz1 = 6
#nctrl_sz2 = 4
#nctrl_szm = 9# =nctrl_sz1+nctrl_sz2-1

# size of complete node sets
nsize1 = 201
nsize2 = 81
nsizem = 261 # nsize1 + nsize2 - nsurface_size

# time steps. set in precice-config.xml //update: step size of mono simulation controlled by ccx, therefore cannot use it for loop length
#nsteps = 50

comp_step = .1

# tolerance for comparing values
tol = 1e-09

##################################################################

def read_dat( dat_path, nsize, first_node, last_node ):
	"""
	Reads values in .dat results file and returns a dictionary with them.
	"""

	print dat_path
	with open(dat_path) as f:
		# keys of beam dict are timesteps. values are nested lists
		# for each node such as: [[# of node, Dx, Dy, Dz], ...]
		beam = {}	
	
		while(True):
			f.readline()
			step_header = f.readline()
			if not(step_header): break
			step = float(step_header.split("time  ")[-1])
			data_type = step_header.strip()[0]
			# initialize list only when reading displacements (first dataset of the node)
			if data_type == "d":
				# (3 displacements + 3 forces) * 261 nodes
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
	return beam


def interface_check( beam1, beam2 ):
	"""
	Compares displacements at the interface nodes, which should be continuous for the two parts of the structure."
	"""

	check_pass = True

	with open( "interface_deltas.csv", 'w' ) as f:
		print "Writing file with interface differences."
		for intf_node in nsurf_indx:
			interface_delta = [abs(x - y) for x,y in zip(beam1[intf_node],beam2[intf_node])]
			if any([x > tol for x in interface_delta]):
				check_pass = False
			f.writelines( ','.join(["%.4e" % x for x in interface_delta]) + '\n' )

	return check_pass


def merge_beam_parts( beam1, beam2 ):
	"""
	Merges beam1 and beam2 into beam_part, taking the mean at the interface."
	"""

	beam_part = [[x+y for x,y in zip(beam1[i],beam2[i])] for i in xrange(261)]
	for i in nsurf_indx:
		beam_part[i] = [(x+y)/2. for x,y in zip(beam1[i],beam2[i])]

	return beam_part


def error_measures( error, beam_mono, beam1path ):
	"""
	Computes L2 norms from the error, and writes output.
	"""

	## relative error
	rel_err = [[xi/(abs(yi+1e-30)) for xi,yi in zip(x,y)] for x,y in zip(error,beam_mono)]

	# global: (L2 norm of the L2 norms of each node's error)
	L2d = math.sqrt(sum([math.sqrt(sum([x*x for x in error[i][:3]])) for i in xrange(261)]))
	L2f = math.sqrt(sum([math.sqrt(sum([x*x for x in error[i][3:]])) for i in xrange(261)])) 
	
	# component-wise: (L2 norm of the vector containing one component of each node's error)
	L2dx = math.sqrt(sum([error[i][0]**2 for i in xrange(261)]))
	L2dy = math.sqrt(sum([error[i][1]**2 for i in xrange(261)]))
	L2dz = math.sqrt(sum([error[i][2]**2 for i in xrange(261)]))
	L2fx = math.sqrt(sum([error[i][3]**2 for i in xrange(261)]))
	L2fy = math.sqrt(sum([error[i][4]**2 for i in xrange(261)]))
	L2fz = math.sqrt(sum([error[i][5]**2 for i in xrange(261)]))

	## output
	print "Displacement errors:"
	for i in xrange(261):
		print "Node", i+1, [": %.4e" % x for x in error[i][:3]]
	print "Relative errors (error/ref.displacement) (using beam_mono displacements as ref.):"
	for i in xrange(261):
		print "Node", i+1, [" %.2f" % x for x in rel_err[i][:3]]	

	print "Force errors"
	for i in xrange(261):
		print "Node", i+1, [": %.4e" % x for x in error[i][3:]]
	print "Relative errors (error/ref.force) (using beam_mono  as ref.):"
	for i in xrange(261):
		print "Node", i+1, [" %.2f" % x for x in rel_err[i][3:]]	
	print "Errors exceed the tolerated value of", tol
	print "Global L2 norm of displacement error =", L2d
	print "L2 norm of component x of displacement error=", L2dx
	print "L2 norm of component y of displacement error=", L2dy
	print "L2 norm of component z of displacement error =", L2dz	
	print "Global L2 norm of force error =", L2f
	print "L2 norm of component x of force error=", L2fx
	print "L2 norm of component y of force error=", L2fy
	print "L2 norm of component z of force error =", L2fz

	with open( "error_vs_convLimit.csv", "a" ) as f:
		f.writelines(','.join([str(x) for x in [ beam1path.split("_")[2], L2d, L2dx, L2dy, L2dz, L2f, L2fx, L2fy, L2fz ]]) + '\n')		

	return

def compare_beam_step( beam1, beam2, beam_mono, tol, beam1path ):
	"""
	Compares displacements & forces, in all nodes, between the beam1_beam2 union and beam_mono. Performs interface check. Computes L2 norms of the error. Returns true if values are equal.
	"""

	if( interface_check( beam1, beam2 ) ):
		print "Interface check successful."
	else:
		print "Discontinuity of displacements at the interface >",tol

	beam_part = merge_beam_parts( beam1, beam2 )

	error = [[abs(xi - yi) for xi,yi in zip(x,y)] for x,y in zip(beam_part,beam_mono)]
	
	if any([any([xi > tol for xi in x]) for x in error]):
		validation_check = False
	else:
		validation_check = True
#		print [[xi  for xi in x] for x in error]

	error_measures( error, beam_mono, beam1path )

	return validation_check


def compare_beam_step_pVSp( beamA1, beamA2, beamB1, beamB2, tol, beam1path ):
	"""
	Compares displacements & forces, in all nodes, between beam A and B. Performs interface check. Computes L2 norms of the error. Returns true if values are equal.
	"""
	if( interface_check( beamA1, beamA2 ) ):
		print "Interface check successful in beam A."
	else:
		print "Discontinuity of displacements at the interface of beam A >",tol

	if( interface_check( beamB1, beamB2 ) ):
		print "Interface check successful in beam B."
	else:
		print "Discontinuity of displacements at the interface of beam B >",tol

	beamA = merge_beam_parts( beamA1, beamA2 )
	beamB = merge_beam_parts( beamB1, beamB2 )

	error = [[abs(xi - yi) for xi,yi in zip(x,y)] for x,y in zip(beamA, beamB)]
	
	if any([any([xi > tol for xi in x]) for x in error]):
		validation_check = False
	else:
		validation_check = True
#		print [[xi  for xi in x] for x in error]

	error_measures( error, beamB, beam1path )

	return validation_check

###############################################################################
################################# MAIN METHODS ##############################################

def validate( beam1path, beam2path, monopath ):

	"Compares results of simulations with a partitioned vs. monolithic setup."

	beam1 = read_dat( beam1path, nsize1, 1, 254 )
	beam2 = read_dat( beam2path, nsize2, 5, 261 )
	beam_mono = read_dat( monopath, nsizem, 1, 261 )

	if( compare_beam_step( beam1[comp_step], beam2[comp_step], beam_mono[comp_step], tol, beam1path ) ):
		print "Validation successful!"
	else: 
		print "Validation unsuccessful."

def part_vs_part( beamA1path, beamA2path, beamB1path, beamB2path ):
	"""
	Compares results of two simulations with partitioned setup."
	"""

	beamA1 = read_dat( beamA1path, nsize1, 1, 254 )
	beamA2 = read_dat( beamA2path, nsize2, 5, 261 )
	beamB1 = read_dat( beamB1path, nsize1, 1, 254 )
	beamB2 = read_dat( beamB2path, nsize2, 5, 261 )

	if( compare_beam_step_pVSp( beamA1[comp_step], beamA2[comp_step], beamB1[comp_step], beamB2[comp_step], tol, beamB1path ) ):
		print "Validation successful!"
	else: 
		print "Validation unsuccessful."

	
#print "----------------BEAM 1 at t=0.5----------------------------"
#print beam1[0.5]
#print "----------------BEAM 2 at t=0.5----------------------------"
#print beam2[0.5]
#print "----------------BEAM MONO at t=0.5-------------------------"
#print beam_mono[0.5]

