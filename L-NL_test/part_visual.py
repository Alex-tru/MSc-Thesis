#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=[ "join", "makediff" ])
args = parser.parse_args()

#### params ####

# size of complete node sets
#nsize1 = 201
#nsize2 = 81
#nsizem = 261 # nsize1 + nsize2 - nsurface_size
#nelem = 32
#nheadermono = 372

#nsize1 = 2225
#nsize2 = 785
#nsizem = 2945 # nsize1 + nsize2 - nsurface_size
#nelem = 512
#nheadermono = 4496

#nsize1 = 14913
#nsize2 = 5121
#nsizem = 19809
#nelem = 4096
#nheadermono = 32112

nsize1 = 4320
nsize2 = 1488
nsizem = 5736
nelem = 11264
nheadermono = 28279

# time steps. set in precice-config.xml
nsteps = 10



##################################################################
def join_frd( frd1, frd2 ):
	"""
	Append the nodes and elements from frd2 to those in frd1 and write the result in a new frd.
	"""
	with open( frd1, "r" ) as f1, open( frd2, "r" ) as f2, open( "pipe_part.frd" , "w" ) as fp:
		
		# copy frd header in new file
		for i in xrange(11):
			fp.write( f1.readline() )
			f2.readline()

		# node header (change number of nodes)
		line_f1 = f1.readline()
		line_f1 = line_f1[:6] + str(nsizem).rjust(30) + line_f1[36:]
		fp.write( line_f1 )
		f2.readline()
		
		# merging node lines. each iteration in the for uses a new line from frd2. lines in frd1 are advanced manually
		line_f1 = f1.readline()
		for line_f2 in iter( f2.readline, " -3\n" ):# -3 indicates end of line block
			# same node in both files (interface): write any (assuming their values are correct!!)
			if line_f1[2] == "3":
				fp.write( line_f2 )
				continue
			if line_f1.split()[1] == line_f2.split()[1]:
				fp.write( line_f1 )
				line_f1 = f1.readline()
			# sorting lines according to node index
			elif line_f2 < line_f1:
				fp.write(line_f2)
			else:
				while(line_f2 > line_f1):
					fp.write( line_f1 )
					line_f1 = f1.readline()
				fp.write( line_f2 )

		fp.write( " -3\n" )

		# element header (change number of elements)
		line_f1 = f1.readline()
		line_f1 = line_f1[:6] + str(nelem).rjust(30) + line_f1[36:]
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
			line_f1 = line_f1[:24] + str(nsizem).rjust(12) + line_f1[36:]
			fp.write( line_f1 )
			f2.readline()
			for j in xrange(5):
				fp.write( f1.readline() )
				f2.readline()

			line_f1 = f1.readline()
			for line_f2 in iter( f2.readline, " -3\n" ):# -3 indicates end of line block
				print "A",line_f1, line_f2
				if line_f1[2] == "3":
					fp.write( line_f2 )
					continue
				# same node in both files (interface): write mean value
				l1_split = line_f1[:13].split() + [ line_f1[13:25], line_f1[25:37], line_f1[37:-1] ]
				l2_split = line_f2[:13].split() + [ line_f2[13:25], line_f2[25:37], line_f2[37:-1] ]
				print l1_split, l2_split
				if l1_split[1] == l2_split[1]:
					# this is an interface node for both beams. write the mean of he values in beam1 and beam2
					print "b",line_f1, line_f2
					mean_vals = [ ( float(x)+float(y) ) / 2. for x,y in zip( [l1_split[2], l1_split[3], l1_split[4]], [l2_split[2], l2_split[3], l2_split[4]] ) ]
					fp.writelines( " -1      " + l1_split[1] + '{:12.5E}'.format(mean_vals[0])+'{:12.5E}'.format(mean_vals[1]) + '{:12.5E}'.format(mean_vals[2]) + '\n' )
					line_f1 = f1.readline()
				# sorting lines according to node index
				elif int(l1_split[1]) > int(l2_split[1]):
					print "Here", l1_split[1], l2_split[1]
					fp.write( line_f2 )
				else:
					while( int(l2_split[1]) > int(l1_split[1]) ):
						print l1_split, l2_split
						print "c",line_f1, line_f2
						fp.write( line_f1 )
						line_f1 = f1.readline()
						if line_f1[2] == "3": break
						l1_split = line_f1[:13].split() + [ line_f1[13:25], line_f1[25:37], line_f1[37:-1] ]
					if l1_split[1] != l2_split[1]:
						fp.write( line_f2 )
					else:
						mean_vals = [ ( float(x)+float(y) ) / 2. for x,y in zip( [l1_split[2], l1_split[3], l1_split[4]], [l2_split[2], l2_split[3], l2_split[4]] ) ]
						fp.writelines( " -1      " + l1_split[1] + '{:12.5E}'.format(mean_vals[0])+'{:12.5E}'.format(mean_vals[1]) + '{:12.5E}'.format(mean_vals[2]) + '\n' )
						line_f1 = f1.readline()

			fp.write(" -3\n")

		fp.write("9999\n")#EOF


def make_diff_frd( frd1, frd2 ):
	"""
	Compute the difference between values of frd1 and frd2, and write the result in a new frd.
	"""
	with open( frd1, "r" ) as f1, open( frd2, "r" ) as f2, open( "pipe_diff.frd", "w" ) as fp:
		
		# copy frd header, node positions and elements, in new file
		for i in xrange(nheadermono):
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
				diff = [ float(x)-float(y) for x,y in zip( [ line1[13:25], line1[25:37], line1[37:49] ], [ line2[13:25], line2[25:37], line2[37:49] ] ) ]
				
				fp.write( line1[:13] + '{:12.5E}'.format( diff[0] ) + '{:12.5E}'.format( diff[1] ) + '{:12.5E}'.format( diff[2]) + '\n' )

			# end of time step
			f1.readline()
			f2.readline()
			fp.write( " -3\n" )

		fp.write( "9999\n" )#EOF


########################## MAIN #################################

if ( args.action == "join" ):
	join_frd( "Calculix1/pipe1.frd", "Calculix2/pipe2.frd" )
elif ( args.action == "makediff" ):
	make_diff_frd( "pipe_part.frd", "pipe_monoNL.frd" )

