#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=[ "join", "makediff" ])
args = parser.parse_args()

#### params ####

# size of complete node sets
nsize1 = 201
nsize2 = 81
nsizem = 261 # nsize1 + nsize2 - nsurface_size

# time steps. set in precice-config.xml
nsteps = 50



##################################################################
def join_frd( frd1, frd2 ):
	"""
	Append the nodes and elements from frd2 to those in frd1 and write the result in a new frd.
	"""
	with open( frd1, "r" ) as f1, open( frd2, "r" ) as f2, open( "beam_part.frd" , "w" ) as fp:
		
		# copy frd header in new file
		for i in xrange(11):
			fp.write( f1.readline() )
			f2.readline()

		# node header (change number of nodes)
		line_f1 = f1.readline()
		line_f1 = line_f1[:33] + str(nsizem) + line_f1[36:]
		fp.write( line_f1 )
		f2.readline()
		
		# merging node lines. each iteration in the for uses a new line from frd2. lines in frd1 are advanced manually
		line_f1 = f1.readline()
		for line_f2 in iter( f2.readline, " -3\n" ):# -3 indicates end of line block
			# same node in both files (interface): write any (assuming their values are correct!!)
			if line_f1[:13] == line_f2[:13]:
				if line_f1[2] == "3": 
					continue
				else:
					fp.write( line_f1 )
					line_f1 = f1.readline()
			# sorting lines according to node index
			elif line_f2 < line_f1:
				fp.write(line_f2)
			else:
				while(line_f2 > line_f1):
					fp.write( line_f1 )
					line_f1 = f1.readline()

				if line_f1[:13] != line_f2[:13]: 
					fp.write( line_f2 )

		fp.write( " -3\n" )

		# element header (change number of elements)
		line_f1 = f1.readline()
		line_f1 = line_f1[:34] + "32" + line_f1[36:]
		fp.write( line_f1 )
		f2.readline()

		# merge element lines. assuming they are sorted and non-overlapping in frd1 and frd2
		for line_f1 in iter( f1.readline, " -3\n" ):	
			fp.write( line_f1 )
		for line_f2 in iter( f2.readline, " -3\n" ):	
			fp.write( line_f2 )
		fp.write( " -3\n" )

		# merging blocks of lines for each step
		for i in xrange( nsteps ):
			print "step", i+1
			# step header
			fp.write( f1.readline() )
			f2.readline()
			line_f1 = f1.readline()
			line_f1 = line_f1[:33] + str(nsizem) + line_f1[36:]
			fp.write( line_f1 )
			f2.readline()
			for j in xrange(5):
				fp.write( f1.readline() )
				f2.readline()

			line_f1 = f1.readline()
			for line_f2 in iter( f2.readline, " -3\n" ):# -3 indicates end of line block
				# same node in both files (interface): write any (assuming their values are correct!!)
				if line_f1[:13] == line_f2[:13]:
					if line_f1[2] == "3":
						continue
					else:
						# this is an interface node for both beams. write the mean of the values in beam1 and beam2
						mean_vals = [ ( float(x)+float(y) ) / 2. for x,y in zip( [line_f1[13:25], line_f1[25:37], line_f1[37:49]], [line_f2[13:25], line_f2[25:37], line_f2[37:49]] ) ]
						fp.writelines( line_f1[:13] + '{:12.5E}'.format(mean_vals[0])+'{:12.5E}'.format(mean_vals[1]) + '{:12.5E}'.format(mean_vals[2]) + '\n' )
						line_f1 = f1.readline()
				# sorting lines according to node index
				elif line_f2 < line_f1:
					fp.write( line_f2 )
				else:
					while( line_f2[:13] > line_f1[:13] ):
						fp.write( line_f1 )
						line_f1 = f1.readline()

					if line_f1[:13] != line_f2[:13]:
						fp.write( line_f2 )
					else:
						mean_vals = [ ( float(x)+float(y) )/2. for x,y in zip( [line_f1[13:25], line_f1[25:37], line_f1[37:49]], [line_f2[13:25], line_f2[25:37], line_f2[37:49]] ) ]
						fp.writelines( line_f1[:13] + '{:12.5E}'.format( mean_vals[0]  )+ '{:12.5E}'.format( mean_vals[1] ) + '{:12.5E}'.format(mean_vals[2]) + '\n' )
						line_f1 = f1.readline()

			fp.write(" -3\n")

		fp.write("9999\n")#EOF


def make_diff_frd( frd1, frd2 ):
	"""
	Compute the difference between values of frd1 and frd2, and write the result in a new frd.
	"""
	with open( frd1, "r" ) as f1, open( frd2, "r" ) as f2, open( "beam_diff.frd", "w" ) as fp:
		
		# copy frd header, node positions and elements, in new file
		for i in xrange(372):
			fp.write( f1.readline() )
			f2.readline()

		# write difference for each step_header
		for i in xrange( nsteps ):
			# write time step header
			for j in xrange(7):
				fp.write( f1.readline() )
				f2.readline()

			# for x node points
			for j in xrange(nsizem): 
				line1 = f1.readline()
				line2 = f2.readline()
				print line1
				print line2
				diff = [ float(x)-float(y) for x,y in zip( [ line1[13:25], line1[25:37], line1[37:49] ], [ line2[13:25], line2[25:37], line2[37:49] ] ) ]
				
				fp.write( line1[:13] + '{:12.5E}'.format( diff[0] ) + '{:12.5E}'.format( diff[1] ) + '{:12.5E}'.format( diff[2]) + '\n' )

			# end of time step
			f1.readline()
			f2.readline()
			fp.write( " -3\n" )

		fp.write( "9999\n" )#EOF


########################## MAIN #################################

if ( args.action == "join" ):
	join_frd( "Calculix1/beam1.frd", "Calculix2/beam2.frd" )
elif ( args.action == "makediff" ):
	make_diff_frd( "beam_part.frd", "CalculixMono/beam_mono.frd" )

