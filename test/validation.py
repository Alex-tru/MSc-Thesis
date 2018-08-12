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

comp_step = .5

# tolerance for comparing values
tol = 1e-06

##################################################################

def read_dat( dat_path, nsize, first_node, last_node ):
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

def compare_beam_step( beam1, beam2, beam_mono, tol ):
	"""
	Compares displacements & forces, in all nodes, between the beam1_beam2 union and beam_mono. Compares the nodes of beam1 and 2 at the interface. Computes L2 norms of the error.
    Returns true if values are equal.
	"""
	
	## interface check
	print "Displacement & force differences (|beam1-beam2|) at the interface nodes:"
	for intf_node in nsurf_indx:
		interface_delta = [abs(x - y) for x,y in zip(beam1[intf_node],beam2[intf_node])]
#		print ["%.4e" % x for x in interface_delta]
#		if any([x > tol for x in interface_delta]):
#			print "Displacements and/or forces do not meet at the interface!"
#			print "Difference:", intf_node+1, ":", ["%.4e" % x for x in interface_delta]
			#do not proceed if there is a discontinuity
#			return False
#		else: print "Interface check ok! (tolerance = ", tol,")"

	## partitioned/monolithic check
	
#	#interface check + joining beam1 and beam2
#	for i in nsurf_indx:
#		if all([abs(x - y) < tol for x,y in zip(beam1[i],beam2[i])]):
#			beam2[i] = [0.,0.,0.]
#		else:
#			print "Displacements are not equal at the interface between beam1 and beam2."
#			print "Node",i,"->   x_beam1 = ",beam1[i],"   x_beam2 = ",beam2[i]
#			return False

	## merge beams
	#since equality at the interface is checked, set interface values of beam1 to 0
	for i in nsurf_indx:
		beam1[i] = [0.,0.,0.,0.,0.,0.]
	beam_part = [[x+y for x,y in zip(beam1[i],beam2[i])] for i in xrange(261)]

	error = [[abs(xi - yi) for xi,yi in zip(x,y)] for x,y in zip(beam_part,beam_mono)]
	if any([any([xi > tol for xi in x]) for x in error]):
#		print [[xi  for xi in x] for x in error]

		## relative error
		rel_err = [[xi/(abs(yi+1e-30)) for xi,yi in zip(x,y)] for x,y in zip(error,beam_mono)]

		## L2_norm

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
#		print "Displacement errors:"
#		for i in xrange(261):
#			print "Node", i+1, [": %.4e" % x for x in error[i][:3]]
#		print "Relative errors (error/ref.displacement) (using beam_mono displacements as ref.):"
#		for i in xrange(261):
#			print "Node", i+1, [" %.2f" % x for x in rel_err[i][:3]]	

#		print "Force errors"
#		for i in xrange(261):
#			print "Node", i+1, [": %.4e" % x for x in error[i][3:]]
#		print "Relative errors (error/ref.force) (using beam_mono  as ref.):"
#		for i in xrange(261):
#			print "Node", i+1, [" %.2f" % x for x in rel_err[i][3:]]	
		print "Errors exceed the tolerated value of", tol
		print "Global L2 norm of displacement error =", L2d
		print "L2 norm of component x of displacement error=", L2dx
		print "L2 norm of component y of displacement error=", L2dy
		print "L2 norm of component z of displacement error =", L2dz	
		print "Global L2 norm of force error =", L2f
		print "L2 norm of component x of force error=", L2fx
		print "L2 norm of component y of force error=", L2fy
		print "L2 norm of component z of force error =", L2fz		
		return False
	
	return True


###############################################################################
################################# MAIN ##############################################


beam1 = read_dat( args.beam1, nsize1, 1, 254 )
beam2 = read_dat( args.beam2, nsize2, 5, 261 )
beam_mono = read_dat( args.mono, nsizem, 1, 261 )

if( compare_beam_step( beam1[comp_step], beam2[comp_step], beam_mono[comp_step], tol ) ):
	print "Validation successful!"
else: 
	print "Validation unsuccessful."

#with open()
#print "----------------BEAM 1 at t=0.5----------------------------"
#print beam1[0.5]
#print "----------------BEAM 2 at t=0.5----------------------------"
#print beam2[0.5]
#print "----------------BEAM MONO at t=0.5-------------------------"
#print beam_mono[0.5]

