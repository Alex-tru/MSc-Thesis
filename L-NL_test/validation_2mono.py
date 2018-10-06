#!/usr/bin/python

"""
Validate results of partitioned against monolithic simulation of the beam test case.
"""

import math

import argparse

parser = argparse.ArgumentParser()
parser.add_argument( "mono1" )
parser.add_argument( "mono2" )
args = parser.parse_args()

############################# params #################################

nsizem = 5736
#nsizem = 19809

step_length = 1e-8

# tolerance for comparing values
tol = 1e-06

##################################################################

def read_dat( dat_path, nsize, comp_step ):
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

def compare_beam_step( beam1, beam2, tol ):
	"""
	Compares displacements & forces, in all nodes, between two beams. Computes L2 norms of the error.
    Returns true if values are equal.
	"""
	
	error = [[abs(xi - yi) for xi,yi in zip(x,y)] for x,y in zip(beam1,beam2)]
	if any([any([xi > tol for xi in x]) for x in error]):
		print "Validation unsuccessful!"
	else: print "Validation successful!"
#		print [[xi  for xi in x] for x in error]

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

	print "Global L2 norm of displacement error =", L2d
#	print "L2 norm of component x of displacement error=", L2dx
#	print "L2 norm of component y of displacement error=", L2dy
#	print "L2 norm of component z of displacement error =", L2dz
#	print "Global L2 norm of force error =", L2f
#	print "L2 norm of component x of force error=", L2fx
#	print "L2 norm of component y of force error=", L2fy
#	print "L2 norm of component z of force error =", L2fz

	return [ L2d, L2dx, L2dy, L2dz, L2f, L2fx, L2fy, L2fz ]

###############################################################################
################################# MAIN ##############################################


with open( "dt_1e-8_NLeff-errorVStime.csv", "w" ) as fw:

	fw.write( "t, L2d, L2dx, L2dy, L2dz, L2f, L2fx, L2fy, L2fz\n" )

	for step_no in range( 100, 10001, 100 ):

		comp_step = round( step_no * step_length, 6 )

		beam1 = read_dat( args.mono1, nsizem, comp_step )
		beam2 = read_dat( args.mono2, nsizem, comp_step )

		L2_errors = compare_beam_step( beam1[comp_step], beam2[comp_step], tol )
		fw.write( ", ".join( [ str(x) for x in [comp_step] + L2_errors ] ) + "\n" )



#with open()
#print "----------------BEAM 1 at t=0.5----------------------------"
#print beam1[0.5]
#print "----------------BEAM 2 at t=0.5----------------------------"
#print beam2[0.5]
#print "----------------BEAM MONO at t=0.5-------------------------"
#print beam_mono[0.5]

