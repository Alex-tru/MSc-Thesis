#!usr/bin/python

"Study of the coupling convergence speed for an experiment run of the precice adapter for calculix."

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument( "dir", help = "Directory with iteration info files to read." )
args = parser.parse_args()

nsteps = 10

# Get the list of elements in the directory
it_files = os.listdir(args.dir)

with open( os.path.join( args.dir, args.dir + "_iterations.csv" ), 'w' ) as fw1:

	# first line is time steps, each line afterwards is data for one experiment
	fw1.write( "time step, " + str( range(1, nsteps+1) )[1:-1] + '\n')

	with open( os.path.join( args.dir, args.dir + "_delColumns.csv" ), 'w' ) as fw2:

		fw2.write( "time step, " + str( range(1, nsteps+1) )[1:-1] + '\n' )

		for fname in it_files:

			if ( fname[-24:] == "iterations-Calculix2.txt" ):

				fw1.write( fname.split('_')[2] + ', ' )
				fw2.write( fname.split('_')[2] + ', ' )

				with open( os.path.join( args.dir, fname ), "r" ) as fr:
					header = fr.readline().split("  ")

					for i in xrange(nsteps):
						line = fr.readline().split("  ")
						fw1.write( line[2] + ', ' )
						fw2.write( line[6] + ', ' )
					fw1.write( '\n' )
					fw2.write( '\n' )
